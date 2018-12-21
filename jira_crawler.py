import urllib3
from bs4 import BeautifulSoup
import os
import re
from datetime import datetime
from issue_tracker import IssueTracker
from patch import Patch
import codecs

def JiraCrawler(project,root_url,issue_id):
    date_format = '%Y-%m-%dT%H:%M:%S'
    http = urllib3.PoolManager()
    urllib3.disable_warnings()

    # project = 'LUCENE'
    # issue_id = 8575
    # root_url = 'https://issues.apache.org/jira/browse/'
    issue_url = os.path.join(root_url, '{}-{}'.format(project,issue_id))
    response = http.request('GET', issue_url)
    web_data = BeautifulSoup(response.data,features="lxml")
    tracker = IssueTracker()
    tracker.id = issue_id

    summary_raw = web_data.title.string
    summary = summary_raw.replace("- ASF JIRA","").replace("[{}-{}]".format(project,issue_id),"").strip()
    tracker.summary = summary


    description = web_data.find(id="description-val").get_text().strip()
    tracker.description = description

    for one_node in web_data.find(id = "issuedetails").find_all('div'):
        key_value_pair = one_node.get_text().split(':')
        if not len(key_value_pair) == 2:
            break
        key = key_value_pair[0].strip()
        value = key_value_pair[1].strip()
        if hasattr(tracker,key.lower()):
            setattr(tracker,key.lower(),value.lower())

    create_time_str = web_data.find(id='datesmodule').find(id='created-val').time['datetime']

    tracker.create_date = datetime.strptime(create_time_str[:-5], date_format)

    update_time_str = web_data.find(id='datesmodule').find(id='updated-val').time['datetime']

    tracker.update_date = datetime.strptime(update_time_str[:-5], date_format)
    
    # Lucene patches
    if web_data.find(id = 'file_attachments') is not None:
        for node in web_data.find(id = 'file_attachments').find_all('div'):
            patch = Patch()
            patch.url = 'https://issues.apache.org'+node.a['href']
            patch.time = datetime.strptime(node.parent.time['datetime'][:-5],date_format)
            patch.id = int(node.parent['data-attachment-id'])
            patch_response = http.request('GET', patch.url)
            patch_data = BeautifulSoup(patch_response.data,features="lxml")
            patch.content = patch_data.get_text()
            matched_lines = [line for line in patch.content.split('\n') if "diff" in line]
            for line in matched_lines:
                strs = line.split(' ')
                file_name = strs[-1][1:]
                patch.touched_files.append(file_name)
            tracker.patch_list.append(patch)
            
    # Zookeeper patches
    if web_data.find_all(attrs ={"class":"link-title"}) is not None:
        for node in web_data.find_all(attrs ={"class":"link-title"}):
            patch = Patch()
            patch.id = int(os.path.basename(node['href']))
            patch.url = node['href']+'.patch'
            patch_response = http.request('GET', patch.url)
            patch_data = BeautifulSoup(patch_response.data,features="lxml")
            patch.content = patch_data.get_text()
            matched_lines = [line for line in patch.content.split('\n') if "diff" in line]
            for line in matched_lines:
                strs = line.split(' ')
                file_name = strs[-1][1:]
                patch.touched_files.append(file_name)
            tracker.patch_list.append(patch)
    # tracker.print()
    return tracker


if __name__ == '__main__':
    project = 'ZOOKEEPER'
    issue_id = 3177
    root_url = 'https://issues.apache.org/jira/browse/'
    tracker = JiraCrawler(project, root_url, issue_id)
    tracker.print()
#    http = urllib3.PoolManager()
#    urllib3.disable_warnings()
#    url_link = 'https://issues.apache.org/jira/browse/ZOOKEEPER-3177'
#    response = http.request('GET', url_link)
#    web_data = BeautifulSoup(response.data,features="lxml")
   
            
        
#    print(web_data)
#    comment_str = web_data.find_all('script')[-3].get_text()
#    s = re.sub(r'\\+', '\\', comment_str)
#    print(comment_str.decode('unicode-escape').encode('utf-8'))
    # comment_node = BeautifulSoup(comment_str,features="lxml")
    # print(comment_node)
    # issue_list_str = web_data.find_all('script')[10].get_text()


    # test_str = '\\"issueKeys\\":[asasaas]'
    # # a = re.search(r'\\"issueKeys\\":\[.\]',test_str)
    # issue_id_list_str = re.search(r'\\"issueKeys\\":\[.*?\]',issue_list_str).group(0)
    # issue_ids = re.findall(r'\\".*?\\"',issue_id_list_str)[1:]
    # for i in issue_ids:
    #     issue_id_str = i.replace('\\"','')
    #     issue_id = issue_id_str[7:]
    #     print(issue_id)
        
    # print(test_str)
