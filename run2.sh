echo $PWD
echo "Setting environment"

# $1 .C file (w/ path if needed)
# $2 output file number


python3 MChistfit.py --filename $1 --run_number $2  #> output.txt 2>error.txt

#command
#./run2.sh [filename] [run_number]
