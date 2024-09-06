import regex as re

file_type_regex=re.compile("\..*")
datatype_regex=re.compile("pdf|json|txt|xlsx")
file_endings=["pdf","json","txt","xlsx","db","csv"]
def determine_file_type(file_name): #vielleicht in einem anderen module?
      #datatype=re.search(datatype_regex,file_name).group()
      for file_ending in file_endings:
            if file_name.endswith(file_ending):
                  return file_ending
      #file_type=file_type_regex.findall(file_name)[0].lstrip(".")
      #return file_type

def strip_file_ending(file_name):
      file_type=determine_file_type(file_name)
      to_strip="."+file_type
      stripped=file_name.replace(to_strip,"")
      return stripped
