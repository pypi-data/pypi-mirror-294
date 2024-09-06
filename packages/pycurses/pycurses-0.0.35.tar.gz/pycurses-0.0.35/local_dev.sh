

function start_dev() {
  dir="src/pycurses"
  result_files=$(grep -rln "^from pycurses." $dir)
  for file in $result_files; do
    sed -i "" "s|from pycurses.|from |g" $file
  done
  echo "Prepared environment for local development"
}

function prepublish() {
  dir="src/pycurses"
  imports=$(ls $dir)

  for import in $imports; do
    import_base_name="${import%.*}"
    if [[ $import_base_name == "__init__" ]]; then
      continue
    fi

    results=$(grep -rln "^from ${import_base_name}" $dir)
    for result in $results; do
      search="from ${import_base_name}"
      replace="from pycurses.${import_base_name}"
      sed -i "" "s|$search|$replace|g" $result
    done
  done
  echo "Prepared environment for publishing environment"
}

function publish() {
  dir="src/pycurses"
  match_line=$(grep "__version__" $dir/__init__.py)
  line_array=($match_line)
  version=${line_array[${#line_array[@]} - 1]}
  numbers=$(echo $version | tr -d '"')
  echo $numbers
  tmp_ifs=$IFS
  IFS="."
  number_arr=($numbers)
  IFS=$tmp_ifs

  update_index=$1
  if [[ $update_index == "" ]]; then
    update_index=2
  fi

  for i in $(seq 0 2); do
    if [[ $i < $update_index ]]; then
      continue
    elif [ $i == $update_index ]; then
      number_to_increment=${number_arr[$i]}
      number_arr[$i]=$((number_to_increment+1))
      echo ${number_arr[$i]}
    else
      number_arr[$i]="0"
    fi
    main_version=${number_arr[0]}
    minor_version=${number_arr[1]}
    update_version=${number_arr[2]}
    new_str="\"${main_version}.${minor_version}.${update_version}\""
    new_line="__version__ = ${new_str}"

    sed -i "" "s/${match_line}/${new_line}/g" $dir/__init__.py
    python3 -m flit publish

  done
}

function main() {
  arg="$1"
  if [[ $arg == "dev" ]]; then
    start_dev
  elif [[ $arg == "prepublish" || $arg == "prepub" ]]; then
    prepublish
  elif [[ $arg == "reinstall" ]]; then
    python3 -m pip install --force-reinstall pycurses
  elif [[ $arg == "publish" || $arg == "pub" ]]; then
    publish $2
  else
    echo "Please pass 'dev' or 'prepub/prepublish', 'publish'/'pub', 'reinstall', to use this script"
  fi
}

main "$@"
