from django.db import models
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

FIBO_0 = 2
FIBO_1 = 3

class NumbersAndSums(models.Model):
    """
    Class that handles communication between the model
    and its corresponding database table fibo_NumbersAndSums
    in the fibo database.

    Attributes:
    - target_num: an integer value denoting the number
    whose Fibonacci decompositions are to be or have
    been calculated.
    - fibo_sums: a string value containing a complete
    list of Fibonacci decompositions for target_num
    separated by ; where each number is separated by ,
    """
    target_num = models.IntegerField()
    fibo_sums = models.TextField()

    @staticmethod
    def get_object_by_target_num(number):
        """
        Static method that gets the object by
        target_num = number. If the object doesn't
        exist in the database (its row
        representation that is), it returns
        None.
        """
        try:
            ns = NumbersAndSums.objects.get(target_num = number)
        except ObjectDoesNotExist:
            ns = None
        return ns

class FiboSequence(models.Model):
    """
    Class that handles communication between the model
    and its corresponding database table fibo_FiboSequence
    in the fibo database. This table can contain one and
    only one row, corresponding to the longest Fibonacci
    sequence that has been calculated so far.

    Attributes:
    - target_num: an integer value denoting the number
    whose Fibonacci decompositions are to be or have
    been calculated.
    - fibo_sums: a string value containing a complete
    list of Fibonacci decompositions for target_num
    separated by ; where each number is separated by ,
    """
    max_num = models.IntegerField()
    fibo_seq = models.TextField()

    @staticmethod
    def get_single_sequence():
        """
        Static method that gets the single row
        in the table. If the row doesn't exist
        in the database, it returns None.
        """
        try:
            fs = FiboSequence.objects.get(id = 1)
        except ObjectDoesNotExist:
            fs = None

        return fs    


class FibonacciSums():
    """
    Class that handles all calculations for Fibonacci
    sums.

    Attributes:
    - number: the target number whose Fibonacci sums
    are to be calculated.
    - fibo_sequence: the longest Fibonacci sequence
    up to number (of type list).
    - sums: a list of lists containing all decompositions
    of number into Fibonacci numbers.
    """
    def __init__(self,number):
        self.number = number
        self.fibo_sequence = []
        self.sums = []


    def __repr__(self,outer_separator, inner_separator):
        """
        Returns a string where sums are separated by
        outer_separator, and numbers of each sum are
        separated by inner_separator. Depending on the
        context these two values may vary.

        Input:
        - outer_separator: a string that will be used
        as list separator.
        - inner_separator: a string that will be used
        as number separator.
        """
        return outer_separator.join([inner_separator.join(str(n) for n in fibo_sum) for fibo_sum in self.sums])
 
    def get_fibo_sequence(self):
        """
        Returns the Fibonacci sequence up to
        self.number.
        Trivial cases are handled first.
        Fetches the sequence on the database. If
        available, and the next element is larger
        than self.number then the sequence is
        sufficient and is immediately returned.
        If the next element is smaller, calculation
        is resumed from the last two elements, and
        is both saved and returned.
        If the sequence is not available on the DB
        (first time using the application or the
        sequence had been deleted), the sequence
        is calculated from FIBO_0 = 2, and FIBO_1 = 3.
        """
        if self.number == 0 or self.number == 1:
            return []
        if self.number == 2:
            return [2]

        fs = FiboSequence.get_single_sequence()

        if fs is not None:
            self.fibo_sequence = [int(n) for n in fs.fibo_seq.split(',') if int(n)<= self.number]
            
            f0 = self.fibo_sequence[-2]
            f1 = self.fibo_sequence[-1]
            f  = f0 + f1
            if f > self.number:
                return self.fibo_sequence
             
        
        else:

            f0 = FIBO_0
            f1 = FIBO_1
            self.fibo_sequence = [f0,f1]
            f  = f0 + f1
        
        while f<=self.number:
            self.fibo_sequence.append(f)
            f0 = f1
            f1 = f
            f = f0 + f1
        fibo_seq = ','.join([str(n) for n in self.fibo_sequence])
        fs = FiboSequence(id=1,max_num=self.number,fibo_seq=fibo_seq)
        fs.save()

        return self.fibo_sequence

    def append_to_all(self,lis,list_of_lists):
        """
        Returns a list of lists whereby a simple
        list (lis) is concatenated with every
        list member of list_of_lists.
        This is useful when calculating Fibonacci
        combinations for a given number self.number.

        Input:
        - lis: a list of numbers
        - list_of_lists: a list of lists
        """
        return [sorted(lis+x) for x in list_of_lists]

    def get_fibo_sums(self):
        """
        Main functionality of the app. Returns a list
        of lists consisting of Fibonacci decompositions
        of self.number.
        
        Calls itself recursively to break down the
        problem into the simpler tasks of calculating
        the same thing for smaller numbers, then
        combining the sums.
        
        Checks trivial cases first.
        
        Calls the sums from the database with self.number
        as the key. If the call fails (the number is
        being calculated for the first time, or its row
        had been deleted), the sum combinations are
        simply recalculated.

        Calculation:
        
        The function gets the Fibonacci sequence up to
        self.number, then iterates over this sequence
        starting with the smallest (2) up to self.number
        divided by 2. Going beyond is pointless, since
        the sum combinations are calculated from smallest
        to largest. A Fibonacci number that exceeds half
        of self.number has only one chance to be part of
        a sum combination, which is that it is equal to
        self.number. This special case is treated at the
        end.

        The function breaks down the problem into solving
        it for self.number minus the current Fibonacci
        number in self.fibo_sequence. This number is
        automatically appended to the solutions of the
        new problem. This will be the case if the difference
        is larger than or equal to the current Fibonacci
        number in the sequence.

        If the difference is smaller, then we backtrack
        and try another Fibonacci number.

        Once out of the loop, the function then checks if
        self.number is not itself a Fibonacci number, and
        adds the singleton [self.number] to the list of
        sums in that case.

        It then saves the number and combinations in the
        database for future use.
        """
        if self.number == 0 or self.number == 1:
            return [[]]
        if self.number==2:
            return [[2]]
        if self.number==3:
            return [[3]]

        ns = NumbersAndSums.get_object_by_target_num(self.number)

        if ns is not None:
            return [[int(n) for n in fibo_sum.split(',')] for fibo_sum in ns.fibo_sums.split(';')]

        self.fibo_sequence = self.get_fibo_sequence()
        i = 0
        self.sums = []
        while self.fibo_sequence[i]<=self.number//2:
            if self.number - self.fibo_sequence[i] >= self.fibo_sequence[i]:
                self.sums += self.append_to_all([self.fibo_sequence[i]],FibonacciSums(self.number-self.fibo_sequence[i]).get_fibo_sums())

            """
            #It looks like backtracking is not needed
            else:
                del self.sums[-1][-1]
            """
            i+=1   

        if self.number in self.fibo_sequence:
            self.sums.append([self.number])
        
        self.save_to_db()
        return self.sums

    def sorting_rule(self,sum_seq,i,max_val):
        """
        Returns a number that will be used as
        a lambda function sorting key in
        adjust_result().

        If the index i is larger than the size
        of sum_seq, we return max_val. Otherwise,
        the value at index i is returned.

        Input:
        - sum_seq: a list of numbers
        - i: a number denoting an index
        - max_val: a number denoting the
        maximum value in a list of lists.
        """
        if len(sum_seq)<i+1:
            return max_val
        else:
            return sum_seq[i]

    def get_max_len(self,res):
        """
        Returns the largest length in a list of
        lists of numbers.
        """
        return max([len(x) for x in res])

    def get_max_val(self,res):
        """
        Returns the largest value in a list of
        lists of numbers.
        """
        return max([max(x) for x in res])

    def adjust_result(self,res):
        """
        Returns an adjusted self.sums whereby the
        lists and the numbers within each list of
        self.sums are sorted according the value
        returned by sorting_rule.

        The lambda function returns a tuple the size
        of the longest list in self.sums, which
        is used to sort the lists by priority, first
        value first, second value second, and so on.

        Edit:
        get_max_val(res) repalced with self.number,
        since the later is always larger than any
        Fibonacci values.
        """
        max_len = self.get_max_len(res)
        self.sums = sorted([x for x in set((tuple(x) for x in res))],key=lambda x:(tuple(self.sorting_rule(x,i,self.number) for i in range(max_len))))
        return self.sums

    def save_to_db(self):
        """
        Saves the object to database. In order not
        to have duplicates, the DB is queried first
        to ensure the object doesn't already exist.
        """
        ns = NumbersAndSums.get_object_by_target_num(self.number)

        if ns is None:
            ns = NumbersAndSums(target_num = self.number,fibo_sums = self.__repr__(';',','))
            ns.save()



if __name__ == '__main__':
    F = FibonacciSums(14)
    print(F.adjust_result(F.get_fibo_sums()))
