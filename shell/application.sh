source_file(){
    source $1
}

add_to_path(){
    if [ ! -d "$1" ]; then
        echo "not a directory "$1
        return
    fi

    if [ ":$STANDIN:" != *":$1:"* ]; then
        STANDIN="${STANDIN:+"$STANDIN:"}$1"
    fi
}

# load all declared environment variables
for file in $(find etc/*.env -type f)
do
    source_file ${file}
done

# append all declared paths to the PATH
for file in $(find etc/*.path -type f)
do
    for path_entry in $(sed -E '$s/(.*\S+.*)/\1\n/' $file)
    do
        add_to_path ${path_entry}
    done
done