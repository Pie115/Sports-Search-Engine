import json
seenPosts = []

with open('myredditdata.json', 'r') as file:
    for line in file:
        data = json.loads(line)

        if(data['id'] not in seenPosts):
            with open("My_Final_Reddit_Data.json", "a") as output_file:
                json.dump(data, output_file)
                output_file.write('\n')
                output_file.flush()    

        if 'id' in data:
            seenPosts.append(data['id'])
                
with open('myredditdata2.json', 'r') as file:
    for line in file:
        data = json.loads(line)

        if(data['id'] not in seenPosts):
            with open("My_Final_Reddit_Data.json", "a") as output_file:
                json.dump(data, output_file)
                output_file.write('\n')
                output_file.flush()   

        if 'id' in data:
            seenPosts.append(data['id'])

with open('myredditdata3.json', 'r') as file:
    for line in file:
        data = json.loads(line)

        if(data['id'] not in seenPosts):
            with open("My_Final_Reddit_Data.json", "a") as output_file:
                json.dump(data, output_file)
                output_file.write('\n')
                output_file.flush()   

        if 'id' in data:
            seenPosts.append(data['id'])