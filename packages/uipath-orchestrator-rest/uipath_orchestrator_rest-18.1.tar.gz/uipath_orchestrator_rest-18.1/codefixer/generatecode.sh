#!usr/bin/bash

# Basic Settings
package_name="uipath_orchestrator_rest"
swagger_url="https://cloud.uipath.com/jcaravaca42/jorge_pruebas/orchestrator_/swagger/v18.0/swagger.json"
package_version="18.0"

data='{
  "options": {
    "packageName": "'"${package_name}"'",
    "packageVersion": "'"${package_version}"'"
  },
  "swaggerUrl": "'"${swagger_url}"'"
}'

tempfolder="tempclient"

echo "----------Generating client--------------"
response=$(curl -s -X POST -H "content-type:application/json" -d "$data" https://generator.swagger.io/api/gen/clients/python)
link=$(echo "$response" | sed -n 's/.*"link":"\([^"]*\)".*/\1/p')

echo "Generated Code Link: $link, downloading"
mkdir -p $tempfolder
curl -o $tempfolder/"${package_name}_${package_version}.zip" "$link"
unzip -q -o "$tempfolder/${package_name}_${package_version}.zip" -d $tempfolder

echo "-----------Unzipped, copying to root directory----------"
destination_path="."
#mkdir -p $destination_path
source_path="$tempfolder/python-client"
cp -r "./$source_path/." "$destination_path"

echo "---------Copied, removing temp client-----------"
rm -r "$tempfolder"

echo "-----Creating python environment---------------"
rm -rf venv
python -m venv venv
sleep 1
source venv/bin/activate
sleep 1
pip install ruff
echo "----Code Validation and autofix------"
rm -f codefixer/ruff_output.txt
ruff_output_file="codefixer/ruff_output.txt"
ruff_command="ruff check --select E9 ."
python_script="python codefixer/extract_info.py"

# Run the loop until the ruff output file is empty
while true; do
    # Run the ruff command and redirect the output to the file
    $ruff_command > "$ruff_output_file"

    # Check if the ruff output is empty
 if [ ! -s "$ruff_output_file" ] || [ "$(head -n 1 "$ruff_output_file")" = "All checks passed!" ]; then
        break  # Exit the loop if the output is either empty or has the first line set to "All checks passed!"
    fi
    echo "----Errors found, fixing---"
    # Run the python script
    $python_script
done

echo "---Code generated! Cleaning up output---"
rm -f codefixer/ruff_output.txt
echo "---Code Successfully generated and fixed!---"
