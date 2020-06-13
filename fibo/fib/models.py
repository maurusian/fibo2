from django.db import models

# Create your models here.

FIBO_0 = 2
FIBO_1 = 3


class FibonacciSums():
    def __init__(self,number):
        self.number = number
        self.fibo_list = []
        self.sums = []

    def get_fibo_list(self):
        if self.number == 2:
            return [2]
        f0 = FIBO_0
        f1 = FIBO_1
        f  = f0 + f1
        self.fibo_list = [f0,f1]
        while f<=self.number:
            self.fibo_list.append(f)
            f0 = f1
            f1 = f
            f = f0 + f1

        return self.fibo_list

    def append_to_all(self,lis,list_of_lists):
        return [sorted(lis+x) for x in list_of_lists]

    def get_fibo_sums(self):
        if self.number==2:
            return [[2]]
        elif self.number==3:
            return [[3]]

        self.fibo_list = self.get_fibo_list()
        i = 0
        self.sums = []
        while self.fibo_list[i]<=self.number//2:
            if self.number - self.fibo_list[i] >= self.fibo_list[i]:
                self.sums += self.append_to_all([self.fibo_list[i]],FibonacciSums(self.number-self.fibo_list[i]).get_fibo_sums())

            elif self.number - self.fibo_list[i] == 0:
                self.sums.append([self.fibo_list[i]])
                        
            else:
                del self.sums[-1][-1]
            i+=1   

        if self.number in self.fibo_list:
            self.sums.append([self.number])
        return self.sums

    def sorting_rule(self,x,i,max_val):
        #print(i)
        #print(x)
        if len(x)<i+1:
            return max_val
        else:
            return x[i]

    def get_max_len(self,res):
        return max([len(x) for x in res])

    def get_max_val(self,res):
        return max([max(x) for x in res])

    def adjust_result(self,res):
        max_len = self.get_max_len(res)
        return sorted([x for x in set((tuple(x) for x in res))],key=lambda x:(tuple(self.sorting_rule(x,i,self.get_max_val(res)) for i in range(max_len))))



if __name__ == '__main__':
    F = FibonacciSums(14)
    print(F.adjust_result(F.get_fibo_sums()))
