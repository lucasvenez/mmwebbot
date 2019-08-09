from webbot import Browser
from lxml import html
from pathlib import Path

import pandas as pd
import time
import os

username = open('.username', 'r').read()
password = open('.password', 'r').read()

####################################################################################
# Accessing web page
####################################################################################
web = Browser()

web.go_to('https://research.themmrf.org')

####################################################################################
# Log in
####################################################################################

web.click('Log In', classname='login_link')

web.type(username, xpath='//*[@id="username"]')

web.type(password, xpath='//*[@id="password"]')

web.click(xpath='//*[@id="fm1"]/div[4]/div/div/div/button')

#
# Got to therapy
#


def parse(identifier, columns, output_path):
    
    result = None
    
    try:

        columns = ['ID'] + columns

        web.go_to('https://research.themmrf.org/rp/explore?mode=table&view=attribute&id={}&level=IA12'.format(identifier))

        time.sleep(5)

        while True:

            tree = html.fromstring(web.get_page_source())

            table = tree.xpath('//*[@id="DT_a_{}"]'.format(identifier))[0]

            data_frame = pd.read_html(html.tostring(table))[0]

            data_frame.columns = columns

            entries = tree.xpath('//*[@id="DT_a_{}_info"]/text()'.format(identifier))[0].split(' ')

            current, limit = int(entries[3].replace(',', '')), int(entries[5].replace(',', ''))

            result = data_frame if result is None else pd.concat([result, data_frame])

            print('Processed {} of {}'.format(current, limit))

            if current < limit:
                web.click('Next')

            else:
                break

        result = result.set_index('ID')

        if not os.path.exists(Path(output_path).parent):
            os.makedirs(Path(output_path).parent)

        result.to_csv(output_path, sep='\t', index=True)
    
    except:
        print('Error while parsing ', identifier)
        
    return result

'''
####################################################################################
# CLINICAL
####################################################################################

#parse('521cff587830a4468ce9f880', ['symptoms'], 'data/clinical/symptoms.tsv')

#
# Adverse Events
#

parse('56bb774458f2287258947326', ['most_common_grade'], 
            'data/clinical/adverse_events/most_common_grade.tsv')

parse('53166272e0d001f0be935e69', ['cmmc'], 
            'data/clinical/adverse_events/cmmc.tsv')

parse('51a4dd2fc026bea0862c6183', ['ecog_ps'], 
            'data/clinical/adverse_events/ecog_ps.tsv')
 
#
# Flow Cytometry Panel
#                                
                               
parse('51a4dd2fc026bea0862c6174', ['percent_aneuploid'], 
            'data/clinical/flow_cytometry_panel/percent_aneuploid.tsv')
            
parse('53166272e0d001f0be935e73', ['percent_plama_cells_bone_marrow'], 
            'data/clinical/flow_cytometry_panel/percent_plama_cells_bone_marrow.tsv')
            
parse('53166272e0d001f0be935e75', ['percent_plama_cells_peripherical_blood'], 
            'data/clinical/flow_cytometry_panel/percent_plama_cells_peripherical_blood.tsv')
            
parse('51a4dd2fc026bea0862c6172', ['cell_markers'], 
            'data/clinical/flow_cytometry_panel/cell_markers.tsv')
            
parse('51a4dd2fc026bea0862c617a', ['dna_index'], 'data/clinical/flow_cytometry_panel/dna_index.tsv')

parse('51a4dd2fc026bea0862c6176', ['lgh'], 
            'data/clinical/flow_cytometry_panel/lgh.tsv')

parse('51a4dd2fc026bea0862c6178', ['lgl'], 
            'data/clinical/flow_cytometry_panel/lgl.tsv')

####################################################################################
# CLINICAL PARAMETERS
####################################################################################

parse('541357527830426568dac026', ['iss'], 
            'data/clinical_params/iss.tsv')

#
# CBC
#

parse('51a4dd2ec026bea0862c6135', ['absolute_neutrophil'], 
            'data/clinical_params/cbc/absolute_neutrophil.tsv')
parse('51a4dd2ec026bea0862c6139', ['platelet'], 
            'data/clinical_params/cbc/platelet.tsv')
parse('51a4dd2ec026bea0862c613b', ['wbc_x10_10_9_l'], 
            'data/clinical_params/cbc/wbc_x10_10_9_l.tsv')
            
#
# Chemistry
#
parse('51a4dd2ec026bea0862c613f', ['bun'], 
            'data/clinical_params/chemistry/bun.tsv')
parse('51a4dd2ec026bea0862c6159', ['crp'], 
            'data/clinical_params/chemistry/crp.tsv')
parse('51a4dd2ec026bea0862c6145', ['glucose'], 
            'data/clinical_params/chemistry/glucose.tsv')
parse('51a4dd2ec026bea0862c6149', ['total_protein'], 
            'data/clinical_params/chemistry/total_protein.tsv')
            
#
# Diagnostic
#
parse('51a4dd2ec026bea0862c613d', ['albumin'], 
            'data/clinical_params/diagnostic/albumin.tsv')
parse('51a4dd2ec026bea0862c6153', ['beta_2_microglobulin'], 
            'data/clinical_params/diagnostic/beta_2_microglobulin.tsv')
parse('51a4dd2ec026bea0862c6141', ['calcium'], 
            'data/clinical_params/diagnostic/calcium.tsv')
parse('51a4dd2ec026bea0862c6143', ['creatinine'], 
            'data/clinical_params/diagnostic.tsv')
parse('51a4dd2ec026bea0862c6137', ['hemoglobin'], 
            'data/clinical_params/diagnostic/hemoglobin.tsv')
parse('51a4dd2ec026bea0862c6147', ['ldh'], 
            'data/clinical_params/diagnostic/ldh.tsv')

####################################################################################
# IMMUNOGLOBULIN PROFILE
####################################################################################

parse('51a4dd2ec026bea0862c614f', ['lga'], 
            'data/immunoglobulin_profile/lga.tsv')
parse('51a4dd2ec026bea0862c6151', ['lgg'], 
            'data/immunoglobulin_profile/lgg.tsv')
parse('51a4dd2ec026bea0862c614b', ['lgl_kappa'], 
            'data/immunoglobulin_profile/lgl_kappa.tsv')
parse('51a4dd2ec026bea0862c6155', ['lgl_lambda'], 
            'data/immunoglobulin_profile/lgl_lambda.tsv')
parse('51a4dd2ec026bea0862c6157', ['lgm'], 
            'data/immunoglobulin_profile/lgm.tsv')
parse('51a4dd2ec026bea0862c614d', ['m_protein'], 
            'data/immunoglobulin_profile/m_protein.tsv')

####################################################################################
# THERAPY
####################################################################################

parse('55c21a8ca7c8d402d0f2f057', ['therapy_first_line_starting_treatment'], 
            'data/therapy/therapy_first_line_starting_treatment.tsv')
parse('524991487830ae7d7f590eea', ['therapy_first_line'], 
            'data/therapy/therapy_first_line.tsv')
parse('524991487830ae7d7f590eec', ['therapy_first_line_class'], 
            'data/therapy/therapy_first_line_class.tsv')
parse('55c21a8ca7c8d402d0f2f055', ['first_line_transpant'], 
            'data/therapy/transplant.tsv')
parse('57c7393ae4b06bbadc19587f', ['therapy_first_line_most_common'], 
            'data/therapy/therapy_first_line_most_common.tsv')

####################################################################################
# CLINICAL OUTCOME
####################################################################################
            
parse('524991487830ae7d7f590ee2', ['disease_status'], 
            'data/clinical_outcome/disease_status.tsv')
            
#
# Treatment Response
#
            
parse('55c21a8ca7c8d402d0f2f06f', ['best_response_fifty_line'], 
            'data/clinical_outcome/treatment_response/best_response_fifty_line.tsv')

parse('5410b4207830e1f92a2afdcb', ['best_response_first_line'], 
            'data/clinical_outcome/treatment_response/best_response_first_line.tsv')

parse('54ed1676a7c8952a8b1f62dc', ['best_response_fourth_line'], 
            'data/clinical_outcome/treatment_response/best_response_fourth_line.tsv')

parse('5410b4207830e1f92a2afdd6', ['best_response_second_line'], 
            'data/clinical_outcome/treatment_response/best_response_second_line.tsv')

parse('54ed1676a7c8952a8b1f62da', ['best_response_third_line'], 
            'data/clinical_outcome/treatment_response/best_response_third_line.tsv')
'''
parse('51a4dd2fc026bea0862c61cd', ['best_response'], 
            'data/clinical_outcome/treatment_response/best_response.tsv')

parse('51a4dd2fc026bea0862c61d5', ['first_response'], 
            'data/clinical_outcome/treatment_response/first_response.tsv')

#
# Time Response
#

parse('51a4dd2fc026bea0862c61e5', ['cycles_to_best_response'], 
            'data/clinical_outcome/time_to_response/cycles_to_best_response.tsv')

parse('51a4dd2fc026bea0862c61bd', ['cycles_to_first_response'], 
            'data/clinical_outcome/time_to_response/cycles_to_first_response.tsv')

parse('51a4dd2fc026bea0862c61dd', ['days_to_best_response'], 
            'data/clinical_outcome/time_to_response/days_to_best_response.tsv')

parse('51a4dd2fc026bea0862c61b5', ['days_to_first_response'], 
            'data/clinical_outcome/time_to_response/days_to_first_response.tsv')

#
# Efficacy Endpoints
#

parse('524991487830ae7d7f590ede', ['overall_survival_status'], 
            'data/clinical_outcome/efficacy_endpoints/overall_survival_status.tsv')
parse('524991487830ae7d7f590ee0', ['progression_free_survivel_status'], 
            'data/clinical_outcome/efficacy_endpoints/progression_free_survivel_status.tsv')

#
# Time to Endpoint
#

parse('53973a6564d0a98496b8e625', ['days_to_overall_survival'], 
            'data/clinical_outcome/time_to_endpoint/days_to_overall_survival.tsv')
parse('53973a6564d0a98496b8e627', ['days_to_disease_progression'], 
            'data/clinical_outcome/time_to_endpoint/days_to_disease_progression.tsv')

####################################################################################
# SeqFISH
####################################################################################

#
# Hyperdiploid Flag
#
parse('57c74561e4b0cb2feed5aa5c', ['hyperdiploid_flag'], 
            'data/fish/hyperdiploid_flag.tsv')

#
# Translocation
#

parse('57c7393ce4b06bbadc195898', ['t_11_14_ccnd1'], 
            'data/fish/translocation/t_11_14_ccnd1.tsv')

parse('57cf37ebe4b07ba7dff6dfaa', ['t_12_14_ccnd2'], 
            'data/fish/translocation/t_12_14_ccnd2.tsv')

parse('57c7393ce4b06bbadc19589c', ['t_14_16_maf'], 
            'data/fish/translocation/t_14_16_maf.tsv')

parse('57c7393ce4b06bbadc19589e', ['t_14_20_mafb'], 
            'data/fish/translocation/t_14_20_mafb.tsv')

parse('57c7393ce4b06bbadc195890', ['t_4_14_whsc1'], 
            'data/fish/translocation/t_4_14_whsc1.tsv')
            
parse('57c7393ce4b06bbadc195892', ['t_6_14_ccnd3'], 
            'data/fish/translocation/t_6_14_ccnd3.tsv')
            
parse('57c7393ce4b06bbadc195896', ['t_8_14_mafa'], 
            'data/fish/translocation/t_8_14_mafa.tsv')

parse('57c7393ce4b06bbadc195894', ['t_8_14_myc'], 
            'data/fish/translocation/t_8_14_myc.tsv')
            
#
# Hyperdiploid Gain
#
parse('57c74561e4b0cb2feed5aa48', ['11p15'], 'data/fish/hyperdiploid_gain/11p15.tsv')
parse('57c74561e4b0cb2feed5aa4c', ['15q15'], 'data/fish/hyperdiploid_gain/15q15.tsv')
parse('57c74561e4b0cb2feed5aa4a', ['19q13'], 'data/fish/hyperdiploid_gain/19q13.tsv')
parse('57c74561e4b0cb2feed5aa50', ['20q13'], 'data/fish/hyperdiploid_gain/20q13.tsv')
parse('57c74561e4b0cb2feed5aa52', ['21q22'], 'data/fish/hyperdiploid_gain/21q22.tsv')
parse('57c74561e4b0cb2feed5aa54', ['3q21'], 'data/fish/hyperdiploid_gain/3q21.tsv')
parse('57c74561e4b0cb2feed5aa56', ['5q31'], 'data/fish/hyperdiploid_gain/5q31.tsv')
parse('57c74561e4b0cb2feed5aa58', ['7q22'], 'data/fish/hyperdiploid_gain/7q22.tsv')
parse('57c74561e4b0cb2feed5aa5a', ['9q33'], 'data/fish/hyperdiploid_gain/9q33.tsv')

#
# Deletions
#
parse('57c74561e4b0cb2feed5aa42', ['13q14'], 'data/fish/deletion/13q14.tsv')
parse('57c74561e4b0cb2feed5aa44', ['13q34'], 'data/fish/deletion/13q34.tsv')
parse('57c74561e4b0cb2feed5aa46', ['17p13'], 'data/fish/deletion/17p13.tsv')

#
# Gains
#
parse('57c74561e4b0cb2feed5aa4e', ['1q21'], 'data/fish/gain/1q21.tsv')

####################################################################################
# Demographics
####################################################################################

parse('58c1e0d1e4b00470116b8a1e', ['age'], 'data/demographics/age.tsv')
parse('58c1e0d1e4b00470116b8a1c', ['gender'], 'data/demographics/gender.tsv')
parse('58c1e0d1e4b00470116b8a22', ['height'], 'data/demographics/height.tsv')
parse('58c1e0d1e4b00470116b8a1a', ['race'], 'data/demographics/race.tsv')
parse('58c1e0d1e4b00470116b8a20', ['weight'], 'data/demographics/weight.tsv')
parse('58c1e0d3e4b00470116b8a51', ['family_cancer'], 'data/demographics/family_cancer.tsv')

