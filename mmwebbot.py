from webbot import Browser
from lxml import html

import pandas as pd
import time

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

    columns = ['ID'] + columns

    web.go_to('https://research.themmrf.org/rp/explore?mode=table&view=attribute&id={}&level=IA12'.format(identifier))

    time.sleep(2)

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

    result.to_csv(output_path, sep='\t', index=True)

    return result

# parse('524991487830ae7d7f590eea', ['THERAPY'], 'data/therapy.tsv')
# parse('524991487830ae7d7f590eec', ['THERAPY_CLASS'], 'data/therapy_class.tsv')

####################################################################################
# TRANSLOCATIONS
####################################################################################

# parse('57c7393ce4b06bbadc195898', ['t_11_14_ccnd1'], 'data/translocation_t_11_14_ccnd1.tsv')
# parse('57cf37ebe4b07ba7dff6dfaa', ['t_12_14_ccnd2'], 'data/translocation_t_12_14_ccnd2.tsv')
# parse('57c7393ce4b06bbadc19589c', ['t_14_16_maf'], 'data/translocation_t_14_16_maf.tsv')
parse('57c7393ce4b06bbadc19589e', ['t_14_16_maf'], 'data/translocation_t_14_16_maf.tsv')


