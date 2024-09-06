

#/
#
from Hemoglycin.adventures.ventures import retrieve_ventures
#
#
#from ventures.clique import ventures_clique
#from Hemoglycin.mixes._clique import mixes_clique
#
#
from .group import clique as clique_group
#
#\

import importlib
#mixes_clique = importlib.import_module ("Hemoglycin.mixes._clique").mixes_clique


def clique ():
	import click
	@click.group ()
	def group ():
		pass

	import click
	@click.command ("example")
	def example_command ():	
		print ("example")

	#group.add_command (example_command)

	#group.add_command (clique_group ())
	#group.add_command (mixes_clique ())
	
	group.add_command (importlib.import_module ("ventures.clique").ventures_clique ({
		"ventures": retrieve_ventures ()
	}))
	
	group ()




#
