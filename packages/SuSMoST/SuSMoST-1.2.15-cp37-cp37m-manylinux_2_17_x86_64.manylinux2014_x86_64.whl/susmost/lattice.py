from susmost.savexyz import save_lattice_as_xyz
from ase.geometry import get_distances
from susmost.make_regr import make_regr
import numpy as np, sys

class Lattice:
	"""
		python -c 'import numpy as np; from susmost import mc, load_lattice_task; lt = load_lattice_task("tmp_00"); lt.set_ads_energy("atop-triang", -1.); m = mc.make_metropolis(lt, 10, [10.], 1.); mc.run(m, 10); print(m.cells, lt.states[0].state_type.__dict__);  l = mc.Lattice(metropolis=m); print(l.calc_fp()); print (l.calc_lateral_energy_per_site()), print (m.curE.internal); print (lt.site_state_types);  print ("PPP",l.calc_property_per_site("ads_energy")) '
	"""
	def __init__(self, lattice_task, lattice_size=None, regr=None, regr_array=None, cells=None):
		if lattice_size is None:
			assert regr is not None
			assert regr_array is not None
			assert cells is not None
			
			self.lattice_task = lattice_task
			self.regr = regr
			self.regr_array = regr_array
			self.cells = cells
		else:
			assert regr is None
			assert regr_array is None
			assert cells is None
			self.lattice_task = lattice_task
			self.regr = make_regr(lattice_size, lattice_task)
			self.regr_array = self.regr.as_nparray(lattice_task.edges_count) # fill regr_array from regr
			self.cells = np.full(len(self.regr), lattice_task.zero_coverage_state_index, dtype=int)	# fill by empty_state_index

	def calc_fp(self):
		n_edges = self.lattice_task.IM_int.shape[1]
		assert n_edges == len(self.lattice_task.edges_dict)
		ei = np.arange(n_edges, dtype=int)
		max_sample_idx = np.max(self.lattice_task.IM_int)
		fp_state_types = np.zeros(len(self.lattice_task.site_state_types))
		fp_list = []
		for i,si in enumerate(self.cells):
			i_sst_idx = self.lattice_task.states[si].state_type.props['idx'].value
			fp_state_types[i_sst_idx] += 1
			j = self.regr_array[i, ei] # neighbours of i-th cell
			sj = self.cells[j] # states of neighbours of i-th cell
			assert len(ei) == len(sj)
			samples = self.lattice_task.IM_int[si, ei, sj]
			assert len(samples) == n_edges
			#print (i, si, samples, j, sj)
			#print (i, si, self.regr[i])
			#assert (si == 0) or (sj == 0) or (samples[0] == -1), f"Interaction over 0-th edge is allways INF_E (-1 index in IM_int): {samples}"
			fp = np.bincount(samples[1:], minlength = max_sample_idx + 1)[1:] # skip 0-th sample as non-representative
			fp_list += [fp]
			#print (i, fp)
		fp_list = np.array(fp_list)
		fp_mean = fp_list.mean(axis=0)
		fp_sigma = fp_list.std(axis=0)
		fp_corr = np.corrcoef(fp_list, rowvar = False)
		fp_state_types /= len(self.cells)

		return fp_state_types, fp_mean, fp_sigma, fp_corr
	
	def calc_lateral_energy_per_site(self, fp_means=None):
		if fp_means is None:
			_, fp_means, _, _ = self.calc_fp()
		sample_energies = self.lattice_task.sample_energies[1:len(fp_means) + 1] # skip 0-th sample as it is allways zero energy
		return np.dot(fp_means,  np.nan_to_num(sample_energies))

	def calc_property_per_site(self, property_name, fp_state_types=None):
		if fp_state_types is None:
			fp_state_types, _, _, _ = self.calc_fp()
		prop_values =  [sst.props[property_name].value for sst in self.lattice_task.site_state_types]
		return np.dot(fp_state_types, prop_values)
		
	def save_cells(self, fn):
		with open(fn, 'w') as f:
			f.write("{}\n\n".format(len(self.cells)))
			for i in range(len(self.cells)):
				state_idx = self.cells[i]
				state_type = self.lattice_task.states[state_idx].state_type
				s = "{}\t{}\t{}\t{}\t{}\n".format(state_type.props['name'].value, state_idx, *self.regr[i].coords)
				f.write(s)
	
	def load_cells_file(self, fn):
		with open(fn, 'r') as f:
			n = int(next(f).strip())
			next(f)
			data = [[s for s in l.split()[1:]] for l in f]
			loaded_cell_state_indices = [int(row[0]) for row in data ]
			loaded_cell_coords = [[float(x) for x in row[1:]] for row in data ]
		return loaded_cell_coords, loaded_cell_state_indices
	
	def set_cells(self, coords, state_indices, cell=None):
		if len(coords) == 0:
			return
		pbc = False if cell is None else True
		self_coords = np.array([self.regr[i].coords for i in range(len(self.cells))])
		Dvec, D = get_distances(coords, self_coords, cell=cell, pbc=pbc)
		nearest_vertices = np.argmin(D, axis=1)
		assert len(nearest_vertices) == len(coords)
		for loaded_i, vertex_i in enumerate(nearest_vertices):
			d = D[loaded_i, vertex_i]
			if d < 1e-3:
				self.cells[vertex_i] = state_indices[loaded_i]
			else:
				raise Exception(f"Nearest point is too far: (self_i, d, loaded_i) = {(self_i, d, loaded_i)}")
	
	def load_cells(self, fn):
		loaded_cell_coords, loaded_cell_state_indices = self.load_cells_file(self, fn)
		self.set_cells(loaded_cell_coords, loaded_cell_state_indices)


	def save_as_xyz(self, fn, comment='', multiplier = [1,1,1], mulmul=0.0):
		return save_lattice_as_xyz(fn, self, comment, multiplier, mulmul)
		
	
