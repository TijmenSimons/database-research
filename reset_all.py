import subprocess


container_name = "b33fc1f2fdea"  # Replace with your container name
command = f"docker exec {container_name} asinfo -v sets -l"

process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = process.communicate()

disk_bytes = 0
if error:
    print(f"Error executing asinfo: {error.decode()}")
else:
    data = output.decode().split("\n")[:-1]
    data = [d.split(":") for d in data]
    data = [{pair.split('=')[0]: pair.split('=')[1] for pair in data_list} for data_list in data]

    for item in data:
        command = f'docker exec {container_name} asinfo -h 127.0.0.1 -v "truncate:namespace=test;set={item["set"]}"'
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            print(error.decode())
        else:
            print(f"[Aspike]: Truncated {item["set"]}")
            print(output.decode())
