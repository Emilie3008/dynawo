from lxml import etree
from islanding_utils.graph_operations import retrieve_islands, remove_disconnected_lines, subgrid_from_grid
from islanding_utils.file_modifications import create_island_IIDM, create_island_par, create_jobs, DydFilter
from islanding_utils.generate_curves import concat_csv, csv_to_js, change_js_filename
import os
import subprocess


class GridEventManager:
    def __init__(self, initial_grid, events, stop_time, name, with_curves = False):
        
        self.name = name
        self.grid = initial_grid
        self.with_curves = with_curves
        self.dynawo_cmd = "dynawo jobs-with-curves" if with_curves else "dynawo jobs"

        self.disconnected_lines = {}
        self.all_events = events
        self.islands = None

        self.critical_time = None
        self.stop_time = stop_time

        self.orig_parfile = "islanding_utils\\Events.par"
        self.parfile = "Events.par"
        self.orig_dydfile = f"islanding_utils\\{name}.dyd"
        self.dydfile = f"{name}.dyd"
        self.working_directory = os.getcwd()

    def initialize(self):
        for line, time in self.all_events.items():
            islands = self.process_event(time, line)
            if islands is not None:
                remaining_events = {evt: t for evt, t in self.all_events.items() if t > time}
                self.islands = self._prepare_island_simulations(islands, remaining_events)
                break

    def run(self):
        self._add_disconnection_events()
        err = self._run_main() 

        if self.islands is None or err==-1:
            return 1

        for island_id, island in enumerate(self.islands, start=1):
            self._run_island(island_id, island[0], island[1])
           
    def _add_disconnection_events(self):
        if self.disconnected_lines == {}:
            tree = etree.parse(self.orig_parfile)
            tree.write(self.parfile, encoding='UTF-8', xml_declaration=True, pretty_print=True)
            tree = etree.parse(self.orig_dydfile)
            tree.write(self.dydfile, encoding='UTF-8', xml_declaration=True, pretty_print=True)

        for event_id, (line, time) in enumerate(self.disconnected_lines.items()):
            if event_id == len(self.disconnected_lines) - 1 and self.islands is not None:
                continue
            self.add_line_disconnection_event(line, time, event_id)

    def add_line_disconnection_event(self, line, time, event_id, type_event="DisconnectLine"):
   
        self._add_event_to_par_file(time, event_id, type_event)
        self._add_model_to_dyd_file(line, event_id, type_event)
        print(f"Disconnection of line {line} added at time {time}s")

    def _add_event_to_par_file(self, time, event_id, type_event):
        tree = etree.parse(self.orig_parfile if event_id == 0 else self.parfile)
        root = tree.getroot()
        namespace = {'dynawo': 'http://www.rte-france.com/dynawo'}
        
        new_event = etree.Element(f"{{{namespace['dynawo']}}}set", id=f"{type_event}{event_id}")
        
        parameters = [
            {'type': 'DOUBLE', 'name': 'event_tEvent', 'value': str(time)},
            {'type': 'BOOL', 'name': 'event_disconnectOrigin', 'value': 'true'},
            {'type': 'BOOL', 'name': 'event_disconnectExtremity', 'value': 'true'}
        ]
        
        for param in parameters:
            etree.SubElement(new_event, f"{{{namespace['dynawo']}}}par", attrib=param)
        
        root.append(new_event)
        tree.write(self.parfile, encoding='UTF-8', xml_declaration=True, pretty_print=True)

    def _add_model_to_dyd_file(self, line, event_id, type_event):
        tree = etree.parse(self.orig_dydfile if event_id == 0 else self.dydfile)
        root = tree.getroot()
        namespace = {'dyn': 'http://www.rte-france.com/dynawo'}
        
        new_model = etree.Element(
            f"{{{namespace['dyn']}}}blackBoxModel",
            id=f"{type_event}{event_id}",
            lib="EventQuadripoleDisconnection",
            parFile=self.parfile,
            parId=f"{type_event}{event_id}"
        )
        
        new_connection = etree.Element(
            f"{{{namespace['dyn']}}}connect",
            id1=f"{type_event}{event_id}",
            var1="event_state1_value",
            id2='NETWORK',
            var2=f"{line}_state_value"
        )
        
        root.append(new_model)
        root.append(new_connection)
        tree.write(self.dydfile, encoding='UTF-8', xml_declaration=True, pretty_print=True)

    def _run_main(self):
        if self.islands is None:
             self.critical_time = self.stop_time
        create_jobs(f"{self.name}.jobs", {"stop_time": self.critical_time}, f"{self.name}.jobs")
        jobs_file_path = os.path.join(self.working_directory, f"{self.name}.jobs")
        r = subprocess.run(f"{self.dynawo_cmd} {jobs_file_path}", cwd=self.working_directory, shell=True,
                           text=True,capture_output=True)
        
        if "DYN Error" in r.stderr:
            print(f"\n Unstable system before islanding :\n{r.stderr}\n")
            return -1

    def _run_island(self, island_id, island, remaining_events):
        
        island_path = f"execution\\island_{island_id}"

        if not os.path.exists(island_path):
            if not os.path.exists("execution"):
                 os.mkdir("execution")
            os.mkdir(island_path)
        
        outputIIDM_path = "outputs\\finalState\\outputIIDM.xml"
        create_island_IIDM(outputIIDM_path, island_id, island, self.disconnected_lines.keys(), 
                          f"{island_path}\\island_{island_id}.xiidm")
        
        dyd_file = DydFilter()
        excluded_gen = dyd_file.create_island_dyd(
            island, self.orig_dydfile, 
            f"{island_path}\\island_{island_id}.dyd", 
            f"{island_path}\\island_{island_id}.par"
        )
        
        create_island_par(f"{self.name}.par", excluded_gen, f"{island_path}\\island_{island_id}.par")
    
        modifications = {
            'job_name': f'{self.name} - Island number {island_id}',
            'iidm_file': f'{island_path}\\island_{island_id}.xiidm',
            'par_file': f'{island_path}\\island_{island_id}.par',
            'dyd_file': f'{island_path}\\island_{island_id}.dyd',
            "initialState": "outputs\\finalState\\outputState.dmp",
            "start_time": self.critical_time,
            'stop_time': self.stop_time,
            'output_dir': island_path
        }
        
        create_jobs(f"{self.name}.jobs", modifications, f"{self.name}_island_{island_id}.jobs")
        
        if remaining_events:
            island_graph = subgrid_from_grid(self.grid, island)
            island_subsim = GridEventManagerIsland(
                island_graph, remaining_events, self.critical_time,
                self.stop_time, self.name, island_id)
            island_subsim.initialize()
            island_subsim.run()
            return 1
        
        jobs_file_path = os.path.join(self.working_directory, 
                                    f"{self.name}_island_{island_id}.jobs")
        
        r=subprocess.run(f"{self.dynawo_cmd} {jobs_file_path}", cwd=self.working_directory, shell=True,
                          text=True,capture_output=True)
        
        if "DYN Error" in r.stderr:
            print(f"\nError for Island {island_id} :\n{r.stderr}\n")
            return -1
        
        if self.with_curves :
            self._process_island_results(island_id)
            print(r.stderr)
  
           

    def _process_island_results(self, island_id):
        island_path = f"execution\\island_{island_id}"
        concat_csv(
            "outputs\\curves\\curves.csv",
            f'{island_path}\\curves\\curves.csv',
            f'outputs\\curves\\island{island_id}.csv'
        )
        
        csv_to_js(
            f'outputs\\curves\\island{island_id}.csv',
            f'outputs\\curves\\curvesOutput\\curves_island{island_id}.js'
        )
        
        change_js_filename(
            "outputs\\curves\\curvesOutput\\curves.html",
            f"outputs\\curves\\curvesOutput\\curves_island{island_id}.html",
            f"curves_island{island_id}.js"
        )

    def process_event(self, event_time, line_event):
        self.disconnected_lines[line_event] = event_time
        self.grid = remove_disconnected_lines(self.grid, line_event)
        islands = retrieve_islands(self.grid)
        
        if len(islands) > 1:
            self.critical_time = event_time
            return islands
        return None

    def _prepare_island_simulations(self, islands, remaining_events):
        return [
            (island, {evt: t for evt, t in remaining_events.items() if evt not in island})
            for island in islands
        ]


class GridEventManagerIsland(GridEventManager):
    def __init__(self, initial_grid, events, start_time, stop_time, name_grid, island_id):
        self.island_id = island_id
        self.name_main_grid = name_grid
        self.start_time = start_time
        self.num_islands = 0
        
        orig_parfile = "islanding_utils\\Events_original.par"
        parfile = f"execution\\island_{island_id}\\Events.par"
        orig_dydfile = f"execution\\island_{island_id}\\island_{island_id}.dyd"
        dydfile = f"execution\\island_{island_id}\\island_{island_id}_.dyd"
        
        super().__init__(
            initial_grid, events, stop_time, f"Island {island_id}",
            orig_parfile, parfile, orig_dydfile, dydfile
        )

    def add_line_disconnection_event(self, line, time, event_id, type_event="DisconnectLine"):
        super()._add_event_to_par_file(time, event_id, type_event)
        
        # Modified version for islands - adds 10 to event_id to avoid conflicts
        tree = etree.parse(self.orig_dydfile if event_id == 0 else self.dydfile)
        root = tree.getroot()
        namespace = {'dyn': 'http://www.rte-france.com/dynawo'}
        
        new_model = etree.Element(
            f"{{{namespace['dyn']}}}blackBoxModel",
            id=f"{type_event}{event_id + 10}",
            lib="EventQuadripoleDisconnection",
            parFile=self.parfile,
            parId=f"{type_event}{event_id}"
        )
        
        new_connection = etree.Element(
            f"{{{namespace['dyn']}}}connect",
            id1=f"{type_event}{event_id + 10}",
            var1="event_state1_value",
            id2='NETWORK',
            var2=f"{line}_state_value"
        )
        
        root.append(new_model)
        root.append(new_connection)
        tree.write(self.dydfile, encoding='UTF-8', xml_declaration=True, pretty_print=True)
        print(f"Disconnection of line {line} added at time {time}s")

    def _run_main(self):
        job_modifications = {
            "start_time": self.start_time,
            "stop_time": self.critical_time if self.critical_time is not None else self.stop_time,
            "initialState": "outputs\\finalState\\outputState.dmp",
            "dyd_file": self.dydfile,
            "job_name": f"{self.name_main_grid} - {self.name} {'(before new islanding)' if self.islands is not None else ''}"
        }
        
        create_jobs(
            f"{self.name_main_grid}_island_{self.island_id}.jobs",
            job_modifications,
            f"{self.name_main_grid}_island_{self.island_id}_main.jobs"
        )
        
        jobs_file_path = os.path.join(
            self.working_directory,
            f"{self.name_main_grid}_island_{self.island_id}_main.jobs"
        )
        
        subprocess.run(f"{self.dynawo_cmd} {jobs_file_path}", cwd=self.working_directory, shell=True)
        
        if self.with_curves:
          self._process_main_results()

    def _process_main_results(self):
        concat_csv(
            'outputs\\curves\\curves.csv',
            f"execution\\island_{self.island_id}\\curves\\curves.csv",
            f'outputs\\curves\\island{self.island_id}_main.csv'
        )
        
        csv_to_js(
            f'outputs\\curves\\island{self.island_id}_main.csv',
            f'outputs\\curves\\curvesOutput\\curves_island{self.island_id}_main.js'
        )
        
        change_js_filename(
            "outputs\\curves\\curvesOutput\\curves.html",
            f"outputs\\curves\\curvesOutput\\curves_island{self.island_id}_main.html",
            f"curves_island{self.island_id}_main.js"
        )

    def _run_island(self, island_id, island, remaining_events):
        self.num_islands = len(self.islands)
        full_island_id = f"{self.island_id}_{island_id}"
        island_path = f"execution\\island_{self.island_id}"
        
        # Prepare files for the island
        outputIIDM_path = os.path.join(f"{island_path}\\finalState\\outputIIDM.xml")
        create_island_IIDM(
            outputIIDM_path, self.island_id, island,
            self.disconnected_lines.keys(),
            f'{island_path}\\island_{full_island_id}.xiidm'
        )
        
        dyd_file = DydFilter()
        excluded_gen = dyd_file.create_island_dyd(
            island, f'{island_path}\\island_{self.island_id}.dyd',
            f'{island_path}\\island_{full_island_id}.dyd',
            f'{island_path}\\island_{full_island_id}.par'
        )
        
        create_island_par(
            f'{island_path}\\island_{self.island_id}.par',
            excluded_gen,
            f'{island_path}\\island_{full_island_id}.par'
        )
        
        # Create job file
        modifications = {
            'job_name': f'{self.name} - Island number {self.island_id} ({island_id}/{self.num_islands})',
            'iidm_file': f'{island_path}\\island_{full_island_id}.xiidm',
            'par_file': f'{island_path}\\island_{full_island_id}.par',
            'dyd_file': f'{island_path}\\island_{full_island_id}.dyd',
            "initialState": f"{island_path}\\finalState\\outputState.dmp",
            "start_time": self.critical_time,
            'stop_time': self.stop_time,
            'output_dir': f'{island_path}\\island_{island_id}'
        }
        
        create_jobs(
            f"{self.name_main_grid}_island_{self.island_id}_main.jobs",
            modifications,
            f'{self.name_main_grid}_island_{full_island_id}.jobs'
        )

        if remaining_events:
            print("More than two islanding situation - pass")
            return

        # Run the simulation
        jobs_file_path = os.path.join(
            self.working_directory, f"{self.name_main_grid}_island_{full_island_id}.jobs"
        )
        
        subprocess.run(f"dynawo jobs-with-curves {jobs_file_path}",
               cwd=self.working_directory,
               shell=True)

        # Process results
        try:
            concat_csv(
                f'outputs\\curves\\island{self.island_id}_main.csv',
                f'{island_path}\\island_{island_id}\\curves\\curves.csv',
                f'outputs\\curves\\island{self.island_id}_final{island_id}.csv'
            )
            
            csv_to_js(
                f'outputs\\curves\\island{self.island_id}_final{island_id}.csv',
                f'outputs\\curves\\curvesOutput\\curves_island{self.island_id}_{island_id}final.js'
            )
            
            change_js_filename(
                "outputs\\curves\\curvesOutput\\curves.html",
                f"outputs\\curves\\curvesOutput\\curves_island{self.island_id}_{island_id}final.html",
                f"curves_island{self.island_id}_{island_id}final.js"
            )
        except Exception:
            print("Something went wrong with the islanding!")