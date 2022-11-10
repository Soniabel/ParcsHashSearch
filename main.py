from Pyro4 import expose
import hashlib

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))
        n,target = self.read_input()
        h=10**(n+1)
        step = h / len(self.workers)

        # map
        mapped = []
        for i in xrange(0, len(self.workers)):
            mapped.append(self.workers[i].mymap(i * step, i * step + step,target))

        # reduce
        reduced = self.myreduce(mapped)
        print("Reduce finished: " + str(reduced))

        # output
        self.write_output(reduced)

        print("Job Finished")

    @staticmethod
    @expose
    def mymap(a, b,target):
        i = a
        res = []
        while i < b:
            hash_object = hashlib.sha1(str(i).encode("utf-8"))
            hex_dig = hash_object.hexdigest()
            if hex_dig == target:
                res.append(str(i))
            i += 1
        return res

    @staticmethod
    @expose
    def myreduce(mapped):
        output = []
        for x in mapped:
            output.extend(x.value)
        return output

    def read_input(self):
        f = open(self.input_file_name, 'r')
        n = int(f.readline())
        target = f.readline()
        f.close()
        return n,target

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        for val in output:
            f.write(val+'\n')
        f.write('\n')
        f.close()