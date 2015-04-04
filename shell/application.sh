add_to_path(){
    if [ ! -d "$1" ]; then
        echo "not a directory "$1
        return
    fi

    if [ ":$PATH:" != *":$1:"* ]; then
        PATH="$1:${PATH:+"$PATH"}"
    fi
}

application_directory='/tmp'
configuration_directory="${application_directory}/etc"

# export all declared environment variables
for file in $(find ${configuration_directory}/*.env -type f)
do
    for path_entry in $(sed -E '$s/(.*\S+.*)/\1\n/' ${file})
    do
        export ${path_entry}
    done
done

# prepend all declared paths to the PATH
for file in $(find ${configuration_directory}/*.path -type f)
do
    for path_entry in $(sed -E '$s/(.*\S+.*)/\1\n/' ${file})
    do
        add_to_path ${path_entry}
    done
done
