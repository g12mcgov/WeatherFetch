import multiprocessing 

def main():
	CPU_COUNT = multiprocessing.cpu_count()
	pool = multiprocessing.Pool(processes=CPU_COUNT-1)
	thing = pool.map(hello, "hi")

def hello(thing):
	print thing

if __name__ == "__main__":
	main()