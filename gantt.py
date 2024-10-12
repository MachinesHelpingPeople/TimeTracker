# Importing the matplotlb.pyplot
import matplotlib.pyplot as plt

import time
import re


def transform_name(name):
	transforms = {
		'.* - gedit$' : 'gedit',
		'.* — Mozilla Firefox \(Private Browsing\)$' : 'Mozilla Firefox (Private Browsing)',
		'.*@.*: ~.*$' : 'Terminal',
	}
	for pattern, target in transforms.items():
		if re.match(pattern, name) is not None:
	#		print ("MATCHING [%s] to [%s]" % (name, target))
			return target

	#print ("MATCHING [%s] to [%s]" % (name, name))
	return name


def create_gantt(date, output):

	# Declaring a figure "gnt"
	fig, gnt = plt.subplots(figsize=(75, 50), dpi=100)

	# Setting labels for x-axis and y-axis
	gnt.set_xlabel('seconds')
	gnt.set_ylabel('Programs')

	events = []


	with open(('data/%s.logs' % date), 'r') as f:
		tmp = []
		tick = 10

		labels = []
		labels_to_tick = {}
		times = []

		ticks = []

		#start = -1

		froms, durations = [], []

		tick_used = False

		switches = [] # bucketed count of switch
		switch_bucket_time = 30

		for line in f:
			tmp.append(line.rstrip())

	#		if len(events) > 200:
	#			break

			if len(tmp) == 1:
				#print (tmp[0])
				label = line.rstrip()#transform_name(line.rstrip())
				labels.append(label)
				if label not in labels_to_tick:
					labels_to_tick[label] = tick
					tick_used = True

			elif len(tmp) == 2:
				times.append(int(line.rstrip()))

				#if start == -1:
				#	start = tmp[1]

				events.append(tmp)
				tmp = []

				froms.append(times[-1] - times[0])
				if len(times) > 1:
					durations.append(times[-1] - times[-2])

				bucket_pos = int(froms[-1] / switch_bucket_time)
				#print ("bucket pos is %d <-- %d / %d" % (bucket_pos, froms[-1], switch_bucket_time))
				while bucket_pos >= len(switches):
					switches.append(0)

				switches[bucket_pos] += 1

				if tick_used:
					tick += 10
					tick_used = False

		gnt.set_yticks(range(10, tick+10, 10))#ticks)
		gnt.set_yticklabels(list(dict.fromkeys(labels)))
		gnt.set_ylim(0, tick+10)
		gnt.set_xlim(0, froms[-1])

		for start, duration, label in zip(froms, durations, labels):
			tick = labels_to_tick[label]
			gnt.broken_barh([(start, duration)], (tick-5, 10))

		s_x, s_y = [], []
		for bucket, switch_count in enumerate(switches):
			# x = bucket * switch_bucket_time
			# y = switch_count
			s_x.append(bucket * switch_bucket_time)
			s_y.append(switch_count * 10)

		#plt.plot([0,10000,15000], [5,50,25], "-", color='red', lw=2.5)
		plt.plot(s_x, s_y, "-", color='red', lw=1.5)


	#print (events)

	# Setting ticks on y-axis
	#gnt.set_yticks([15, 25, 35])
	# Labelling tickes of y-axis
	#gnt.set_yticklabels(['1', '2', '3'])

	# Setting graph attribute
	gnt.grid(True)



	"""
	# Declaring a bar in schedule
	gnt.broken_barh([(40, 50)], (30, 9), facecolors =('tab:orange'))

	# Declaring multiple bars in at same level and same width
	gnt.broken_barh([(110, 10), (150, 10)], (10, 9),
		                     facecolors ='tab:blue')

	gnt.broken_barh([(10, 50), (100, 20), (130, 10)], (20, 9),
		                              facecolors =('tab:red'))
	"""

	fig.subplots_adjust(
	top=0.88,
	bottom=0.11,
	left=0.2,
	right=0.9,
	hspace=0.2,
	wspace=0.2
	)



	if output == 'file':
		#plt.savefig(time.strftime('reports/%Y-%m-%d.gantt.png'))
		plt.savefig('reports/%s.gantt.png' % date)
	else:
		plt.show()

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--date', type=str, default='today')
	parser.add_argument('--output', type=str, default='file')
	parser.add_argument('--limit', type=int, default=-1)
	args = parser.parse_args()

	date = time.strftime('%Y-%m-%d') if args.date == 'today' \
	 else time.strftime('%Y-%m-%d', time.gmtime(time.time() - (int(args.date)*24*60*60)))

	create_gantt(date=date, output=args.output)

