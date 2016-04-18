
import random
import re
from optparse import OptionParser

class CE:
	def __init__(self, minv, maxv):
		self.min = minv
		self.max = maxv
		self.exlist=list()

class Condition:
	def __init__(self, sum_min = 0, sum_max=200, big_min=0, big_max=6, odd_min = 0, odd_max =6, prime_min=0, prime_max=6, span = 17):
		self.sum = CE(sum_min, sum_max)
		self.sum_min = sum_min
		self.sum_max = sum_max
		self.big_min = big_min
		self.big_max = big_max
		self.odd_min = odd_min
		self.odd_max = odd_max
		self.prime_min = prime_min
		self.prime_max = prime_max
		self.span = span
		
		pass

class DC:
	#init function
	def __init__(self):
		self.red=list()
		self.blue=list()
		self.number=0
		self.sum=0
		self.big=0
		self.odd=0
		self.prime=0
		self.mod10_sum =0
		self.mod3_sum=0
		self.fct={}
		self.bfct={}
		self.ch={}
		self.bch={}
		pass
	
	#append a red number
	def append_red(self, red):
		m = 17
		
		prime_list=list((1,2,3,5,7,11,13,17,19,23,27,29,31))
		for r in self.red:
			if r == red:
				return
		
		self.red.append(red)
		self.red.sort()
		self.sum = self.sum+red
		self.mod10_sum = self.mod10_sum +red%10
		self.mod3_sum = self.mod3_sum +red%3
		if red >m:
			self.big =self.big+1
		if red%2 > 0:
			self.odd = self.odd+1
		
		if prime_list.count(red) > 0:
			self.prime = self.prime+1
		
	
	
	#append a blue number
	def append_blue(self, blue):
		for b in self.blue:
			if b == blue:
				return
		
		self.blue.append(blue)
		self.blue.sort()

	#string
	def toString(self):
		s = ""
		for r in self.red:
			if r < 10:
				s = s + '0'
			
			s = s + str(r)+","
		
		for b in self.blue:
			if b < 10:
				s = s+'0'
			s = s + str(b)+","
		
		s=s+"sum:"+str(self.sum)+" big:"+str(self.big) + " odd:"+str(self.odd) + "prime:"+str(self.prime)+ "span:"+str(self.span())+"fct:"+str(self.fct)+"ch:"+str(self.ch)
		return s
	
	#
	def cmp_red(self, red):
		count = 0
		for r1 in self.red:
			for r2 in red:
				if r1==r2:
					count=count+1
		
		return count
	def cmp_hist_red(self, hist, loop, counter):
		if loop == -1:
			for d in hist:
				if self.cmp_red(d.red) >= counter:
					return True
		else:
			for i in range(0,loop):
				d = hist[i]
				if self.cmp_red(d.red) >= counter:
					return True
		
		return False
	
	def span(self):
		return self.red[-1] - self.red[0]
		
	def list_lot(self):
		l = len(self.red)
		lenb = len(self.blue)
		dl = list()
		for r1 in range(0, l):
			for r2 in range(r1+1, l):
				for r3 in range(r2+1,l):
					for r4 in range(r3+1, l):
						for r5 in range(r4+1, l):
								for b1 in range(0,lenb):
									for b2 in range(b1+1, lenb):
										dc = DC()
										dc.append_red(self.red[r1])
										dc.append_red(self.red[r2])
										dc.append_red(self.red[r3])
										dc.append_red(self.red[r4])
										dc.append_red(self.red[r5])
										dc.append_blue(self.blue[b1])
										dc.append_blue(self.blue[b2])
										dl.append(dc)
		return dl
	
	
	def list(self):
		return self.list_lot()
		
	
	def is_suitable(self, condition):
		if self.sum < condition.sum.min or self.sum > condition.sum.max or self.sum in condition.sum.exlist:
			return False
		if self.big < condition.big_min or self.big > condition.big_max:
			return False
		if self.odd < condition.odd_min or self.odd > condition.odd_max:
			return False
		if self.prime < condition.prime_min or self.prime > condition.prime_max:
			return False
		
		if self.span() < condition.span:
			return False
		return True
	
	def list_suitable(self, condition):
		l = self.list()
		for d in l:
			if d.is_suitable(condition):
				pass
			else:
				return False
		
		return True

	
def calculate_hist(dc_list):
	rt={}
	listlen = len(dc_list)
	rangelist=range(0,listlen)
	rlen=5
	
	for i in rangelist:
		if dc_list[i].number != 0:
			if dc_list[i].number not in rt.keys():
				rt[dc_list[i].number] = 0
			rt[dc_list[i].number] = rt[dc_list[i].number] +1
		for j in range(i+1,listlen):
			dc1=dc_list[i]
			dc2=dc_list[j]
			for r1 in dc1.red:
				for r2 in dc2.red:
					if r1==r2:
						if(r1 not in dc1.fct):
							dc1.fct[r1]=1
						dc1.fct[r1]=dc1.fct[r1]+1
			#blue
			for b1 in dc1.blue:
				for b2 in dc2.blue:
					if b1 == b2:
						if b1 not in dc1.bfct:
							dc1.bfct[b1]=1
						else:
							dc1.bfct[b1]=dc1.bfct[b1]+1
			m=(j-i)%listlen
			if m not in dc1.ch:
				dc1.ch[m] = len(dc1.fct.keys())
			if m not in dc1.bch:
				dc1.bch[m]= len(dc1.bfct.keys())
			if 	len(dc1.fct.keys()) == rlen:
				#print dc1.toString()
				break
			
	return rt


def open_lottery(filename):
	dc_list=list()
	lotfile = open(filename)
	
	while(1):
		s = lotfile.readline()
		if s == "":
			break
		
		dc = DC()
		m=re.match(r"(?P<no>\d+)\s+(?P<r1>\d+)\s+(?P<r2>\d+)\s+(?P<r3>\d+)\s+(?P<r4>\d+)\s+(?P<r5>\d+)\s+\+\s+(?P<b1>\d+)\s+(?P<b2>\d+)", s)
		dc.append_red(int(m.group("r1")))
		dc.append_red(int(m.group("r2")))
		dc.append_red(int(m.group("r3")))
		dc.append_red(int(m.group("r4")))
		dc.append_red(int(m.group("r5")))
		
		dc.append_blue(int(m.group("b1")))
		dc.append_blue(int(m.group("b2")))
		dc_list.append(dc)
	
	lotfile.close()
	return dc_list


def generate_dc(t,rl, r, bl, b):
	
	dc = DC()
	
	random.seed()
	
	rs = random.sample(rl, r)
	
	for r1 in rs:
		dc.append_red(r1)
				
	random.seed()
	bs = random.sample(bl, b)
	
	for b1 in bs:
		dc.append_blue(b1)
		
	return dc

def list_all_dc(hist_list, condition):
	l=34
	dl=list()
	for r1 in range(1, l):
		for r2 in range(r1+1, l):
			for r3 in range(r2+1,l):
				for r4 in range(r3+1, l):
					for r5 in range(r4+1, l):
						for r6 in range(r5+1,l):
							dc=DC('dc')
							dc.append_red(r1)
							dc.append_red(r2)
							dc.append_red(r3)
							dc.append_red(r4)
							dc.append_red(r5)
							dc.append_red(r6)
							if dc.is_suitable(condition) == False:
								continue
							if dc.cmp_hist_red(hist_list, -1, 5):
								continue
							#dl.append(dc)
							print dc.toString()
	return dl
	

	
def count_red(t,l):
	rd={}
	rng=range(1,36)
	
	for i in rng:
		rd[i]=0
	for d in l:
		for r in d.red:
			rd[r] = rd[r]+1
	
	return rd
def count_blue(t,l):
	rd={}
	if t == 'dc':
		rng=range(1,17)
	elif t =='lot':
		rng=range(1,13)
	else:
		return None
	for i in rng:
		rd[i]=0
	for d in l:
		for r in d.blue:
			rd[r] = rd[r]+1
	
	return rd
def count_redc(l):
	print len(l)
	rd={}
	
	for d in l:
		rs = 0
		for r in d.red:
			rs = rs*16+r
		if rs not in rd.keys():
			rd[rs]=0
		rd[rs] = rd[rs]+1
	
	return rd
def count_bluec(l):
	print len(l)
	rd={}
	
	for d in l:
		rs = 0
		for r in d.blue:
			rs = rs*16+r
		if rs not in rd.keys():
			rd[rs]=0
		rd[rs] = rd[rs]+1
	
	return rd
def show_hist(hist):
	for h in hist:
		print h.toString()
	
def stat(hist, idx):
	rt={}
	for h in hist:
		if idx in h.ch.keys():
			if h.ch[idx] not in rt:
				rt[h.ch[idx]] = 0
			rt[h.ch[idx]]=rt[h.ch[idx]]+1
	return rt
def bstat(hist, idx):
	rt={}
	for h in hist:
		if idx in h.bch.keys():
			if h.bch[idx] not in rt:
				rt[h.bch[idx]] = 0
			rt[h.bch[idx]]=rt[h.bch[idx]]+1
	return rt
	

def method( dc_list, rl,r,bl,b, condition,c):
	global noquiet
	total_loop = 0
	result = list()
	while c > 0:
		total_loop = total_loop+1
		if(total_loop > 618):
			print "total %d" %total_loop
			break
		random.seed()
		if len(rl) < r :
			rl = range(1,36)
		if len(bl) < b:
			bl = range(1,13)
		
		dc = generate_dc(type,rl, r, bl, b)	
		dc_list_1 = dc_list
		
		if dc.cmp_hist_red(dc_list_1, -1, 5):
			if noquiet:
				print "EEEEE",dc.toString()
			continue
		
		
		if dc.cmp_hist_red(dc_list_1, r, 2):
			if noquiet:
				print "FFFFF",dc.toString()
			continue
		if dc.list_suitable( condition) == False:
			if noquiet:
				print "NNNNN",dc.toString()
			continue
		
		result.append(dc)
		
		c = c-1
		
		for i in dc.red:
			rl.remove(i)
		for i in dc.blue:
			bl.remove(i)
	return result

def method1( dc_list, rl,r,bl,b, condition,c, idx):
	st = stat(dc_list, idx)
	bst = bstat(dc_list, idx)
	t=0
	bt = 0
	p=list()
	bp=list()
	for i in st.values():
		t=t+i
		p.append(t)
	for i in bst.values():
		bt = bt+i
		bp.append(bt)
	rll=list()
	for i in range(0,idx):
		for ri in dc_list[i].red:
			if ri not in rll:
				rll.append(ri)
			if ri in rl:
				rl.remove(ri)
	
	bll=list()
	for i in range(0,idx):
		for bi in dc_list[i].blue:
			if bi not in bll:
				bll.append(bi)
			if bi in bl:
				bl.remove(bi)
	print rll, rl, bll
	pi=0
	bpi=0
	total_loop = 0
	result = list()
	
	while(c>0):
		total_loop = total_loop+1
		if(total_loop > 61800):
			break
		random.seed()
		dc=DC()
		rn=random.randrange(0,t)
		t1=0
		bt1=0
		for i in st.keys():
			t1 = t1+st[i]
			if rn <= t1:
				pi = i
				#print pi
				break
		pi = min(len(rll),pi)
		for ri in random.sample(rll, pi):
			dc.append_red(ri)
		for ri in random.sample(rl, r-pi):
			dc.append_red(ri)
		
		bn = random.randrange(0, bt)
		for i in bst.keys():
			bt1 = t1+bst[i]
			if bn < bt1:
				bpi = i
				break
			
		bpi = min(len(bll), bpi)
		#print bpi
		for bi in random.sample(bll, bpi):
			dc.append_blue(bi)
		for bi in random.sample(bl,b-bpi):
			dc.append_blue(bi)
			
		if dc.list_suitable( condition) == False:
			if noquiet:
				print "NNNNN",dc.toString()
			continue
		if dc.cmp_hist_red(dc_list, r, 1):
			if noquiet:
				print "FFFFF",dc.toString()
			continue
		
		result.append(dc)
		c = c-1
		
		for i in dc.red:
			if i in rl:
				rl.remove(i)
			if i in rll:
				rll.remove(i)
				
		for i in dc.blue:
			if i in bl:
				bl.remove(i)
			if i in bll:
				bll.remove(i)
	return result
def process_default( filename):
	rt={}		
	return rt	
				

def process_lot( options):
	
	filename = options.filename or 'lottery.txt' 
	rt=process_default( filename)
	if options.rednumber == None:
		rt['r'] = 5
	else:
		rt['r'] = int(options.rednumber)
	
	if options.bluenumber == None:
		rt['b'] = 2
	else:
		rt['b'] = int(options.bluenumber)
		
	
	rt['condition']=Condition(45,145,1,4,1,4,0,4,13)
	
	rt['dc_list'] = open_lottery(filename)
	rt['rl'] = range(1,36)
	rt['bl'] = range(1,13)
	rt['last'] = 0
	rt['s'] = 0
	rt['e'] = 35
	return rt	


	
if __name__ == "__main__":
	parser=OptionParser()
	parser.add_option("-f", "--file", dest="filename", help="history file name", metavar="filename")
	parser.add_option("-r", "--red", dest="rednumber", help="red number", metavar="rednumber")
	parser.add_option("-b", "--blue", dest="bluenumber", help="blue number", metavar="bluenumber")
	parser.add_option("-c", "--count", dest="countnumber", help="count number", metavar="countnumber")
	parser.add_option("-t", "--type", dest="type", help="lottery type", metavar="type")
	parser.add_option("-m", "--method", dest="method", help="generate method", metavar="method")
	parser.add_option("-d", "--debug", dest="debug", help="debug mode", metavar="debug")
	parser.add_option("-q", "--quiet", dest="quiet", help="quiet mode", metavar="quiet")
	(options, args) = parser.parse_args()
	
	sum_dist={}
	sum10={}
	sum3={}	
	debug = 0
	
		
	if options.countnumber == None:
		c = 5
	else:
		c = int(options.countnumber)
		
	if options.quiet == None:
		noquiet = 0
	else:
		noquiet = 1
	
	pd = process_lot( options)
		
	if options.method == None:
		m = 0
	else:
		m = int(options.method)
		
	if options.debug == None:
		debug = 0
	else:
		debug = int(options.debug)
		
		
	dc_list = pd['dc_list']
	condition = pd['condition']
	if debug !=0:
		
		rd = count_redc(dc_list)
		rds = rd.keys()
		rds.sort()
		for d in rds:
			print hex(d), rd[d]
	r = pd['r']
	b = pd['b']
	rl = pd['rl']
	bl = pd['bl']
	last=pd['last']
	s=pd['s']
	e=pd['e']
	
	rt = calculate_hist(dc_list)
	#show_hist( dc_list)
	#for i in rt.keys():
	#	print hex(i),rt[i]
	for i in range(1,10):
		print stat(dc_list, i), bstat(dc_list, i)
	if type == 'lot' and debug == 1:
		rd = count_bluec(dc_list)
		rds = rd.keys()
		rds.sort()
		for d in rds:
			print hex(d), rd[d]
	#list_all_dc(dc_list, condition)
	
	
	rd = count_red(type, dc_list)
		
	for d in dc_list:
		if d.sum not in sum_dist:
			sum_dist[d.sum]=0
		sum_dist[d.sum] = sum_dist[d.sum]+1
		if d.mod10_sum not in sum10:
			sum10[d.mod10_sum] = 1
		else:
			sum10[d.mod10_sum] = sum10[d.mod10_sum]+1
		if d.mod3_sum not in sum3:
			sum3[d.mod3_sum] = 1
		else:
			sum3[d.mod3_sum] = sum3[d.mod3_sum]+1
	
		
	for i in range(0, r):
		condition.sum.exlist.append(dc_list[i].sum)
		
	print condition.sum.exlist
	
	if m ==0:
		rs = method( dc_list, rl,r,bl,b,condition,c)
	else:
		rs = method1( dc_list, rl,r,bl,b,condition,c,m)
		
	for d in rs:
		print d.toString()

