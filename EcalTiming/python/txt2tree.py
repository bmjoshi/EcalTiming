import ROOT
import array

import sys

type_map = {
		"B": "i",
		"b": "i",
		"S": "i",
		"s": "i",
		"I": "i",
		"i": "i",
		"F": "f",
		"D": "f",
		"L": "i",
		"l": "i",
		"O": "i",
}

def txt2tree(input,tree,format):
	types = [a.split(':') for a in format.split(',')]
	ncolumns = len(types)
	data = [[]]*ncolumns
	for i in range(ncolumns):
		name,t = types[i]
		pytype = type_map[t]
		data[i] = array.array(pytype,[0])
		tree.Branch(name,data[i],name + '/' + t)

	with open(input,'r') as f:
		for line in f:
			line = line.split()
			for i in range(ncolumns):
				name,t = types[i]
				x = line[i]
				if type_map[t] is 'i':
					xtype = int
				if type_map[t] is 'f':
					xtype = float
				data[i][0] = xtype(x)
			tree.Fill()
	print("Loaded tree with", tree.GetEntries())
	print(tree.Show(0))
	print(tree.Show(1))
	print(tree.Show(2))



if __name__ == "__main__" :
	#Parse Arguments
	argc = len(sys.argv)
	if argc < 4:
		print("Usage: tree2txt.py <input.txt> <output.root> <tree> <format>")
		print("<format> = name1:type1,name2:type2")
		print("ex: tree2txt.py input.txt output.root MyTree nevents:I,energy:F")
		sys.exit(-1)

	input = sys.argv[1]
	output = sys.argv[2]
	tree_path = sys.argv[3]
	format = sys.argv[4]

	tree = ROOT.TTree(tree_path,"Tree made from " + input)
	txt2tree(input,tree,format)
	file = ROOT.TFile.Open(output,"RECREATE")
	tree.Write()
	file.Write()
