
import greedypacker


if __name__ == '__main__':
    #                           width, height
    M = greedypacker.BinManager(10, 6, pack_algo='guillotine', heuristic='best_shortside', rotation=False, sorting=False)
    print("Hello")