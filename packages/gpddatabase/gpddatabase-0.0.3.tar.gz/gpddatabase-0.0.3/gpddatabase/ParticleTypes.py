from particle import Particle
from particle import ParticleNotFound

from gpddatabase.Exceptions import ExceptionUnknownType
from gpddatabase.Exceptions import ExceptionAmbiguousParticle

class ParticleTypes:

	'''Class defining particle types. Uses python 'particle' library.'''

	def check_type(self, value):

		'''Check if type exist. If not, raise exception.'''

		try:

			Particle.findall(value)

			particles = Particle.findall(value)

			if len(particles) != 1 and value != "p":
				raise ExceptionAmbiguousParticle(value)

		except ParticleNotFound as err:
			raise ExceptionUnknownType(value) from err

	def get_description(self, value):

		'''Get description of a given type.'''

		try:

			particles = Particle.findall(value)

			if len(particles) != 1 and value != "p":
				raise ExceptionAmbiguousParticle(value)

			return particles[0].name

		except ParticleNotFound as err:
			raise ExceptionUnknownType(value) from err

	def get_particle(self, value):

		'''Get 'Particle' object (see 'particle' library) for a given type.'''

		try:
			particles = Particle.findall(value)

			if len(particles) != 1 and value != "p":
				raise ExceptionAmbiguousParticle(value)

			return particles[0]

		except ParticleNotFound as err:
			raise ExceptionUnknownType(value) from err
