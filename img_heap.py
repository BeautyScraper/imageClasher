# Python3 implementation of Max Heap
from logging import debug
from random import randint
import sys
import pandas as pd
from pathlib import Path
# Python3 implementation of Max Heap
from functools import total_ordering

# def get_index(list_a, index,default_value= Candidate(0,'dump.jpg')):
# 	try:
# 		return list_a[index]
# 	except:
 


@total_ordering
class Candidate:
	def __init__(self, key_worth, filepath):
		self.key_worth = int(key_worth)
		self.filepath = filepath

	def __lt__(self, other):
		return self.key_worth<other.key_worth

	def __eq__(self, other):
		return self.key_worth == other.key_worth

	def __le__(self, other):
		return self.key_worth<= other.key_worth
	
	def __ge__(self, other):
		return self.key_worth>= other.key_worth
		
	def __ne__(self, other):
		return self.key_worth != other.key_worth

	def __repr__(self) -> str:
		return f'{self.key_worth}  FIlepath:  {self.filepath}'

class MaxHeap:
	def __enter__(self):
		return self

	def __init__(self,csv_filepath):
		self.csv_filepath = csv_filepath
		# self.maxsize = maxsize
		self.size = -1
		if Path(csv_filepath).is_file():
			self.csv_to_heap()
		else:
			self.Heap = [Candidate(0,'dump.jpg')] 
			self.Heap[0] = Candidate(sys.maxsize,'dump.jpg')
			self.FRONT = 1

	def csv_to_heap(self):
		df = pd.read_csv(self.csv_filepath)
		self.Heap = []
		for i,_ in enumerate(df['key_worth']):
			self.Heap.append(Candidate(df.iloc[i]['key_worth'],df.iloc[i]['filepath'])) 
			self.size += 1
		# self.Heap[0] = Candidate(sys.maxsize,'dump.jpg')
		self.FRONT = 1
		# return df

	def heap_to_csv(self):
		df = pd.DataFrame(columns=['key_worth','filepath'])
		for i,_ in enumerate(self.Heap):
			df.loc[i] = [self.Heap[i].key_worth,self.Heap[i].filepath]
		df.to_csv(self.csv_filepath,index=False)

	def __exit__(self, exc_type, exc_val, exc_tb):
		# breakpoint()
		self.heap_to_csv()
		return True
	# Function to return the position of
	# parent for the node currently
	# at pos
	def insert_child_to_parent(self, parent, child):
		# breakpoint()
		self.size += 1
		self.Heap.append(child) 

		current = self.size 

		# breakpoint()
		while (parent.filepath !=
			self.Heap[self.parent(current)].filepath):
			print(f'parent: {self.Heap[self.parent(current)].filepath}  current: {self.Heap[current].filepath}')
			self.swap(current, self.parent(current))
			current = self.parent(current)


	def parent(self, pos):
		
		return pos // 2

	# Function to return the position of
	# the left child for the node currently
	# at pos
	def leftChild(self, pos):
		
		return 2 * pos

	# Function to return the position of
	# the right child for the node currently
	# at pos
	def rightChild(self, pos):
		
		return (2 * pos) + 1

	# Function that returns true if the passed
	# node is a leaf node
	def __del__(self):
		# self.heap_to_csv()
		# print(self.csv_filepath)
		return True

	def isLeaf(self, pos):
		
		if pos >= (self.size//2) and pos <= self.size:
			return True
		return False

	# Function to swap two nodes of the heap
	def swap(self, fpos, spos):
		
		self.Heap[fpos], self.Heap[spos] = (self.Heap[spos],
											self.Heap[fpos])

	# Function to heapify the node at pos
	def maxHeapify(self, pos):

		# If the node is a non-leaf node and smaller
		# than any of its child
		if not self.isLeaf(pos):
			if (self.Heap[pos] < self.Heap[self.leftChild(pos)] or
				self.Heap[pos] < self.Heap[self.rightChild(pos)]):

				# Swap with the left child and heapify
				# the left child
				if (self.Heap[self.leftChild(pos)] >
					self.Heap[self.rightChild(pos)]):
					self.swap(pos, self.leftChild(pos))
					self.maxHeapify(self.leftChild(pos))

				# Swap with the right child and heapify
				# the right child
				else:
					self.swap(pos, self.rightChild(pos))
					self.maxHeapify(self.rightChild(pos))
	def traverse_heap(self):
		current = len(self.Heap)
		while (current > 0):
			current = self.parent(current)
			yield self.Heap[current]
		# if current == 0:
		# 	yield self.Heap[current]

	# Function to insert a node into the heap
	def insert(self, element):
		
		# if self.size >= self.maxsize:
		# 	return
		# breakpoint()
		self.size += 1
		self.Heap.append(element) 

		current = self.size 

		# breakpoint()
		while (self.Heap[current] >=
			self.Heap[self.parent(current)]):
			self.swap(current, self.parent(current))
			current = self.parent(current)
		# breakpoint()

	# Function to print the contents of the heap

	def Print(self):
		
		for i in range(1, (self.size // 2) + 1):
			try:
				print("PARENT : " + str(self.Heap[i])) 
				print("LEFT CHILD : " + str(self.Heap[2 * i]) )
				print("RIGHT CHILD : " + str(self.Heap[2 * i + 1]))
			except:
				continue

	# Function to remove and return the maximum
	# element from the heap
	def extractMax(self):

		popped = self.Heap[self.FRONT]
		self.Heap[self.FRONT] = self.Heap[self.size]
		self.size -= 1
		self.maxHeapify(self.FRONT)
		
		return popped

# Driver Code
if __name__ == "__main__":
	
	print('The maxHeap is ')
	
	# maxHeap = MaxHeap('hello.csv')
	with MaxHeap('hello.csv') as maxHeap:
	# with open('hello1.csv','w') as fp:
		maxHeap.Print()
		# maxHeap.insert(Candidate(randint(5,100),'XXX.jpg'))
		# maxHeap.insert(Candidate(randint(5,100),'XXX.jpg'))
		# maxHeap.insert(Candidate(randint(5,100),'XXX.jpg'))
		# maxHeap.insert(Candidate(randint(5,100),'XXX.jpg'))
		# maxHeap.insert(Candidate(randint(5,100),'XXX.jpg'))
		# maxHeap.insert(Candidate(randint(5,100),'XXX.jpg'))
		# maxHeap.insert(Candidate(randint(5,100),'XXX.jpg'))
		# maxHeap.insert(Candidate(randint(5,100),'XXX.jpg'))
		# maxHeap.insert(Candidate(randint(5,100),'XXX.jpg'))
		# maxHeap.heap_to_csv()
		# maxHeap.Print()
		th = maxHeap.traverse_heap()
		print( [x for x in th])
		breakpoint()		
		print("The Max val is " + str(maxHeap.extractMax()))
