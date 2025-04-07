import os 
from lxml import etree
import pypowsybl as pp
import re


def create_island_IIDM(outputIIDM, id_island, elements_island, disconnected_lines, to_iidm):
    network = pp.network.load(outputIIDM)
    network.remove_elements(list(disconnected_lines))
    network.remove_elements(elements_island)

    network.save(to_iidm)

    with open(to_iidm, "r", encoding='utf-8') as file:
        content = file.read()

    content = re.sub(
        r'<iidm:network xmlns:iidm="http://www\.powsybl\.org/schema/iidm/1_\d+" id="[^"]+"',
        f'<iidm:network xmlns:iidm="http://www.itesla_project.eu/schema/iidm/1_0" id="ISLAND{id_island}"',
        content,
        1  
    )
    content = re.sub(
        r' minimumValidationLevel="[^"]*"',
        '',
        content
    )
    with open(to_iidm, "w", encoding='utf-8') as file:
        formatted = format_xml_file(content)
        file.write(formatted)

def format_xml_file(to_format):
    to_format = re.sub(
        r'<iidm:operationalLimitsGroup(\d+) id="[^"]+">\s*<iidm:currentLimits permanentLimit\d*="([^"]+)"/>\s*</iidm:operationalLimitsGroup\d+>',
        lambda m: f'<iidm:currentLimits{m.group(1)} permanentLimit="{m.group(2)}"/>',
        to_format
    )
    
    to_format = re.sub(
        r' selectedOperationalLimitsGroupId\d*="[^"]*"',
        '',
        to_format
    )
    to_format = re.sub(
        r'<iidm:substation id="[^"]*"/>',
        '',
        to_format
    )

    to_format = re.sub(
        r'<iidm:shunt id="([^"]+)"(?: sectionCount="(\d+)")?(?: voltageRegulatorOn="[^"]+")? bus="([^"]+)" connectableBus="([^"]+)" q="([^"]+)">\s*<iidm:shuntLinearModel bPerSection="([^"]+)" maximumSectionCount="([^"]+)"/>\s*</iidm:shunt>',
        lambda m: f'<iidm:shunt id="{m.group(1)}" bPerSection="{m.group(6)}" maximumSectionCount="{m.group(7)}" currentSectionCount="{m.group(2) or "1"}" bus="{m.group(3)}" connectableBus="{m.group(4)}" q="{m.group(5)}"/>',
        to_format
    )
    
    return to_format

class DydFilter:
    def __init__(self):
        self.i = 0  # Variable d'instance au lieu d'une globale
        
    def create_island_dyd(self, other_island, from_dyd, to_dyd, parFile):
        with open(from_dyd,"r", encoding='utf-8') as file:
            content = file.read()
        filtered, angles = self.filter_dyd(content, other_island, parFile)
        with open(to_dyd, "w") as file:
            file.write(filtered)
        return angles

    def filter_dyd(self, xml_content, exclude_list, parFile):
        lines = xml_content.split('\n')
        result = []
        skip_block = False
        excluded_angles = []
        i = 0  # Compteur pour la renumérotation
        
        groups_to_exclude = set()
        
        # Première passe pour identifier les groupes à exclure
        for line in lines:
            if 'dyn:connect' in line:
                id1_match = re.search(r'id1="([^"]+)"', line)
                id2_match = re.search(r'id2="([^"]+)"', line)
                var1_match = re.search(r'var1="[^_]+_(grp|node)_(\d+)"', line)
                
          
                if ((id1_match.group(1) in exclude_list) or 
                    (id2_match.group(1) in exclude_list)) and var1_match:
                    groups_to_exclude.add(int(var1_match.group(2)))
        

        for line in lines:
            if '<dyn:blackBoxModel' in line and "OMEGA_REF" not in line:
                id = re.search(r'id="([^"]+)"', line)
                static_id = re.search(r'staticId="([^"]+)"', line) 
                if static_id is None: 
                    result.append(line)
        
                elif (( id.group(1) in exclude_list) and 
                    (static_id.group(1) in exclude_list)):
                    if "/>" not in line:
                       skip_block = True
                    continue
                result.append(line)
                continue

            if skip_block:
                if '</dyn:blackBoxModel>' in line:
                    skip_block = False
                continue
                
     
            if 'id="OMEGA_REF"' in line and 'parFile=' in line:
                parFile = parFile.replace('\\', '/')
                line = re.sub(r'parFile="[^"]+"', f'parFile="{parFile}"', line)
                self.i = 0  # Réinitialisation du compteur
                result.append(line)
                continue
            
         
            if 'dyn:connect' in line:
                id1_match = re.search(r'id1="([^"]+)"', line)
                id2_match = re.search(r'id2="([^"]+)"', line)
                var1_match = re.search(r'var1="([^_]+)_(grp|node)_(\d+)"', line)
                
                # Exclusion si:
                # - id1 ou id2 est dans exclude_list
                # - OU fait partie d'un groupe marqué pour exclusion
                should_exclude = (
                    (id1_match and id1_match.group(1) in exclude_list) or
                    (id2_match and id2_match.group(1) in exclude_list) or
                    (var1_match and int(var1_match.group(3)) in groups_to_exclude)
                )
                
                if should_exclude:
                    if var1_match and var1_match.group(2) == "grp":
                        num = int(var1_match.group(3))
                        if num not in excluded_angles:
                            excluded_angles.append(num)
                    continue
                
                # Renumérotation pour OMEGA_REF
                if id1_match and id1_match.group(1) == "OMEGA_REF":
                    def replace_num(match):
                      
                        prefix = match.group(1)
                        suffix = match.group(2)
                        new_num = self.i//4
                        self.i += 1
                        return f'var1="{prefix}_{suffix}_{new_num}"'
                    
                    line = re.sub(r'var1="(omega|omegaRef|numcc|running)_(grp|node)_\d+"', replace_num, line)
                
                result.append(line)
                continue
            
            # On conserve toutes les autres lignes non traitées
            result.append(line)
        
        return '\n'.join(result), excluded_angles



def create_island_par(from_par, excluded_generators, to_par):
    with open(from_par,"r", encoding='utf-8') as file:
        par_content = file.read()
    
    if excluded_generators == []:
        with open(to_par,"w") as file:
            file.write(par_content)
    set_pattern = re.compile(r'(<set id="OmegaRef">.*?</set>)', re.DOTALL)
    set_match = set_pattern.search(par_content)
    
    if not set_match:
        return par_content 
    
    original_set = set_match.group(1)
    modified_set = original_set
    
    nb_gen_pattern = re.compile(r'(<par type="INT" name="nbGen" value=")\d+(")')
    
    current_nb_gen = int(re.search(r'<par type="INT" name="nbGen" value="(\d+)"', modified_set).group(1))

    new_nb_gen = current_nb_gen - len(excluded_generators)
    modified_set = nb_gen_pattern.sub(rf'\g<1>{new_nb_gen}\2', modified_set)
    

    for index in sorted(excluded_generators, reverse=True):
        weight_pattern = re.compile(rf'<par type="DOUBLE" name="weight_gen_{index}" value="[^"]+"/>\s*')
        modified_set = weight_pattern.sub('', modified_set)

    remaining_weights = [i for i in range(current_nb_gen) if i not in excluded_generators]
    
    def renumber_weights(match):
        nonlocal remaining_weights
        old_index = int(match.group(1))
        if old_index in remaining_weights:
            new_index = remaining_weights.index(old_index)
            return f'<par type="DOUBLE" name="weight_gen_{new_index}" value="{match.group(2)}"'
        return match.group(0)
    
    modified_set = re.sub(
        r'<par type="DOUBLE" name="weight_gen_(\d+)" value="([^"]+)"',
        renumber_weights,
        modified_set
    )

    modified_set = re.sub(r'\n\s*\n', '\n', modified_set)
    
 
    par_content = par_content.replace(original_set, modified_set)
    
    with open(to_par, "w") as file:
        file.write(par_content)


def create_jobs(jobsFile, modifications, to_jobsFile):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(jobsFile, parser) 
    root = tree.getroot()
    
    if 'job_name' in modifications:
        job = root.find('.//{http://www.rte-france.com/dynawo}job')
        if job is not None:
            job.set('name', modifications['job_name'])
    
    if 'iidm_file' in modifications or 'par_file' in modifications:
        network = root.find('.//{http://www.rte-france.com/dynawo}network')
        if network is not None:
            if 'iidm_file' in modifications:
                network.set('iidmFile', modifications['iidm_file'])
            if 'par_file' in modifications:
                network.set('parFile', modifications['par_file'])


    if 'dyd_file' in modifications:
        dyn_models = root.find('.//{http://www.rte-france.com/dynawo}dynModels')
        if dyn_models is not None:
            dyn_models.set('dydFile', modifications['dyd_file'])
    
    simulation = root.find('.//{http://www.rte-france.com/dynawo}simulation')
    if simulation is not None:
        if 'start_time' in modifications:
            simulation.set('startTime', str(modifications['start_time']))
        if 'stop_time' in modifications:
            simulation.set('stopTime', str(modifications['stop_time']))

    
    if 'output_dir' in modifications:
        outputs = root.find('.//{http://www.rte-france.com/dynawo}outputs')
        if outputs is not None:
            outputs.set('directory', modifications['output_dir'])
            
    if "solver_file" in modifications:
        solver = root.find('.//{http://www.rte-france.com/dynawo}solver')
        if solver is not None:
            solver.set('parFile', modifications['solver_file'])

    if "curves_file" in modifications:
        curves = root.find('.//{http://www.rte-france.com/dynawo}curves')
        curves.set("inputFile", modifications["curves_file"])

    modeler = root.find('.//{http://www.rte-france.com/dynawo}modeler')
    if modeler is not None and "initialState" in modifications:
      
        existing_initialState = modeler.find('{http://www.rte-france.com/dynawo}initialState')
        
        if existing_initialState is not None:
        
            existing_initialState.set("file", modifications["initialState"])
        else:
          
            initialState = etree.Element("{http://www.rte-france.com/dynawo}initialState")
            initialState.set("file", modifications["initialState"])
            

            dyn_models = modeler.find('{http://www.rte-france.com/dynawo}dynModels')
            if dyn_models is not None:
                dyn_models.addnext(initialState)
            else:
                modeler.append(initialState)


    namefile = to_jobsFile
    
    with open(namefile, 'wb') as f:
        f.write(b'<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n')
        for comment in root.xpath('//comment()'):
            comment_text = f'<!--{comment.text}-->'.encode('utf-8')
            f.write(comment_text + b'\n')
        f.write(etree.tostring(root, pretty_print=True, encoding='utf-8'))


