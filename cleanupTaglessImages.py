import json
import os

token = os.environ['GITHUB_TOKEN']
containerName = os.environ['containerName']

cmd = "curl -s -H \"Accept: application/vnd.github.v3+json\" -H \"Authorization: token " + token + "\" https://api.github.com/user/packages/container/" + containerName + "/versions > temp.json"
os.system(cmd)

with open('temp.json') as f:
  contents = f.read()

response = json.loads(contents)

taglessImages = []
for i in range(len(response)):
    tags = response[i]['metadata']['container']['tags']
    if (len(tags) == 0):
        taglessImages.append(response[i]['id'])
if (len(taglessImages) == 0):
    print("No tagless images to delete.")
else:
    for i in range(len(taglessImages)):
        cmd = "curl -X DELETE -H \"Accept: application/vnd.github.v3+json\" -H \"Authorization: token " + token + "\" https://api.github.com/user/packages/container/" + containerName + "/versions/"
        id = str(taglessImages[i])
        cmd += id
        print("Deleting " + id)
        os.system(cmd)
    print("Done.")

os.system("rm ./temp.json")