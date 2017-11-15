import numpy
import sys 

class Incr:
	@property
	def rangoneg(self):
		return self._rangoneg
	@rangoneg.setter
	def rangoneg(self, rango):
		self._rangoneg = 1 + rango

	def calcincome(actualincome):
		return self._rangoneg * actualincome

	def __init__(self, rangonegocio):
		self.rangoneg = numpy.array([rangoneg.min, rangonegocio.max])


class Negociacion:
	
	def __call__(self, value):
		return value*(1+numpy.array([self._min,self._max]))
	def __init__(self, min=.15, max=.20):
		self._min = min
		self._max = max

class LiquidadorSalario:


	def __init__(self, income, riesgo=1, independiente=1):

		ssocial = {
		'empleado':	{'salud':.04,'pension':.04},
		'empleador':{'salud':.085,'pension':.12, 'arp':[.00522,.01044,.02436,0.0435,0.0696]}}

		prestaciones = {'primaservicio' : .083333, 'cesantias' : .083333, 'vacaciones' : .0417}

		parafiscales = {'icbf':0.03, 'sena':0.02, 'caja':0.04}
		retfuente = 0.04
		self.saludtotal = ssocial['empleador']['salud'] + ssocial['empleado']['salud']
		self.saludtotal *= income
		self.saludempleado = ssocial['empleado']['salud'] * income
		self.saludempleador = ssocial['empleador']['salud'] * income
		
		self.pensiontotal = ssocial['empleador']['pension'] + ssocial['empleado']['pension']
		self.pensiontotal *= income
		self.pensionempleado = ssocial['empleado']['pension'] * income
		self.pensionempleador = ssocial['empleador']['pension'] * income
		
		self.arptotal = ssocial['empleador']['arp'][riesgo] * income
		
		self.primatotal = prestaciones['primaservicio'] * income
		self.cesantiastotal = prestaciones['cesantias'] * income
		
		self.interesescesantias = self.cesantiastotal * 30 * .12 * income 
		self.interesescesantias /= 360
		
		self.vacacionestotal = prestaciones['vacaciones'] * income

		self.icbftotal = parafiscales['icbf'] * income
		self.senatotal = parafiscales['sena'] * income
		self.cajatotal = parafiscales['caja'] * income
		
		self.income = income

		self.totalsintegral = self.saludtotal + self.pensiontotal + self.arptotal + self.primatotal + self.cesantiastotal + self.interesescesantias + self.vacacionestotal + self.icbftotal + self.senatotal + self.cajatotal
		self.totalsservicios = self.saludtotal + self.pensiontotal + self.arptotal + self.primatotal + self.cesantiastotal + self.interesescesantias + self.vacacionestotal 

		self.employeecost = self.saludempleado + self.pensionempleado
		if independiente == 0:
			self.employeercost = self.totalsintegral - self.employeecost
		else:
			self.employeercost = self.totalsservicios - self.employeecost

		self.liquidacionempleadonnoret = self.income + self.employeercost

		self.liquidacionempleadonret = self.liquidacionempleadonnoret / (1 - retfuente)

		self.carga = self.liquidacionempleadonret - self.income 
		self.retfuente = self.liquidacionempleadonret - self.liquidacionempleadonnoret


if __name__ == "__main__":

	print ("+Nomina+")
	print (sys.argv)
	
	try: 
		income = float(sys.argv[1])
	except:
		income = 7.5
	
	try:
		minplus = float(sys.argv[2])

	except:
		minplus = .10

	try: 
		maxplus = float(sys.argv[3])
	except:
		maxplus = .15

	rango = Negociacion(minplus,maxplus)
	incomeplus = rango(income)

	print ("actual income: ", income)
	print ("new income range: ", rango(income))

	liquid = LiquidadorSalario(incomeplus)
	for key in liquid.__dict__.keys():
		print (key,liquid.__dict__[key])


