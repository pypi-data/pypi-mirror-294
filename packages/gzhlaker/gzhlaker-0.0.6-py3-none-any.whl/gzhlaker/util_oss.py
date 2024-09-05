import os
import pickle
import sys
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider

def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r{0}% '.format(rate), end='')
        sys.stdout.flush()

def check_and_upload(source_path, target_path, file_list, use_env_variable = False, ass_key = None, ass_secret = None):
    if file_list is []:
        return 
    if use_env_variable == True:
        auth = oss2.ProviderAuthV4(EnvironmentVariableCredentialsProvider())
    else:
        auth = oss2.AuthV4(ass_key, ass_secret)
    bucket = oss2.Bucket(auth, 'https://oss-cn-huhehaote.aliyuncs.com', 'gzhlaker-experiment', region="cn-huhehaote")
    
    for item in file_list:
        if type(item) == str:
            file_name, file_description = item, None
        else:
            file_name, file_description = item

        oss_path = os.path.join(target_path, file_name)
        local_path = os.path.join(source_path, file_name)
        readme_path = os.path.join(target_path, "readme.txt")
        
        resule_position = 0
        
        oss_exists = bucket.object_exists(oss_path)
        local_exists = os.path.exists(local_path)
        
        if local_exists and not oss_exists:
            bucket.put_object_from_file(oss_path, local_path, progress_callback=percentage)
            if file_description is not None:
                resule = bucket.append_object(readme_path, resule_position, f"{file_name}:{file_description}\n")
                resule_position = resule.next_position
        elif oss_exists and not local_exists:
            bucket.get_object_to_file(oss_path, local_path, progress_callback=percentage)
        elif not oss_exists and not local_exists:
            print("无可用文件")

def get_file_name(path):
  """
  获取一个文件夹下的所有名称
  """
  files = []
  for file in os.listdir(path):
      files.append(file)
  return files

def check_path(path):
    if not os.path.exists(path):
        os.system(f"mkdir -p {path}")


def save_pickle(path, target):
    with open(path, mode="wb") as f:
        pickle.dump(target, f)

def load_pickle(path):
    with open(path, mode="rb") as f:
        data = pickle.load(f)
    return data