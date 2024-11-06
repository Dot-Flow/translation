import os


def main():
    with open('validate_list.txt', 'w') as f:
        # for i in os.listdir('data/annotations/'):
        #     f.write('data/annotations/' + i + '\n')
        for i in range(1, 50):
            f.write('data/annotations/성북소식지' + str(i).zfill(2) + '.json\n')
    
    
if __name__ == '__main__':
    main()