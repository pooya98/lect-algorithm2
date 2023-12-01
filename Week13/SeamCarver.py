from pathlib import Path
from PIL import Image  # PIL (Python Image Library)
import math
import random
import timeit

class SeamCarver:
    MAX_ENERGY = 1000.0 # Static constant

    def __init__(self, image):
        assert(isinstance(image, Image.Image))
        self.image = image.copy() # Create a copy to not mutate the original image

    def width(self):
        return self.image.size[0]
    
    def height(self):
        return self.image.size[1]

    def energy(self, x, y):
        assert(x>=0 and x<self.width() and y>=0 and y<self.height())
        if x==0 or x==self.width()-1 or y==0 or y==self.height()-1: return self.MAX_ENERGY
        pixels = self.image.load()
        cl, cr = pixels[x-1,y], pixels[x+1,y]
        cu, cd = pixels[x,y-1], pixels[x,y+1]
        return int(math.sqrt((cl[0]-cr[0])**2 + (cl[1]-cr[1])**2 + (cl[2]-cr[2])**2 +\
            (cu[0]-cd[0])**2 + (cu[1]-cd[1])**2 + (cu[2]-cd[2])**2))

    def energeMap(self): # return all energe in string format
        rlist = []
        for row in range(self.height()):
            clist = []
            for col in range(self.width()):
                clist.append(f"{self.energy(col,row):4.0f}")
            rlist.append(' '.join(clist))
        return '\n'.join(rlist)

    def energyMapWithVerticalSeam(self, seam):
        assert(self.isValidSeam(seam))
        rlist = []
        energySum = 0.0
        for row in range(self.height()):
            clist = []
            for col in range(self.width()):
                if col == seam[row]: 
                    clist.append(f"{self.energy(col,row):3.0f}*")
                    energySum += self.energy(col,row)
                else: clist.append(f"{self.energy(col,row):4.0f}")
            rlist.append(' '.join(clist))
        rlist.append(f"energy sum over vertical seam: {energySum:4.0f}")
        return '\n'.join(rlist)

    def energySumOverVerticalSeam(self, seam):        
        assert(self.isValidSeam(seam))
        energySum = 0.0
        for row in range(self.height()):
            energySum += self.energy(seam[row],row)
        return energySum

    @staticmethod
    def isListOfIntegers(x):
        if isinstance(x, list):
            if all(isinstance(e, int) for e in x): return True
            else: return False
        else: return False

    def isValidSeam(self, seam):        
        if not SeamCarver.isListOfIntegers(seam): return False
        if len(seam) != self.height(): return False
        for i in range(self.height()):
            if seam[i]<0 or self.width()<=seam[i]: return False
            if i>0 and (seam[i] < seam[i-1]-1 or seam[i-1]+1 < seam[i]): return False
        return True

    def removeVerticalSeam(self, seam):
        # Sanity check
        assert(self.isValidSeam(seam))        
        assert(self.width() > 1)

        # Add codes below
        carvedImage = Image.new("RGB", (self.width()-1, self.height()), "white")
        pixelsInCarvedImage = carvedImage.load()
        pixelsInOriginalImage = self.image.load()
        for row in range(self.height()):
            colInCarvedImage = 0
            for col in range(self.width()):
                if col == seam[row]: continue
                pixelsInCarvedImage[colInCarvedImage,row] = pixelsInOriginalImage[col,row]
                colInCarvedImage += 1

        self.image = carvedImage

    def findVerticalSeam(self):
        # Add codes below
        h = self.height()
        w = self.width()
        distTo = [[0 for _ in range(w)] for _ in range(h)]
        edgeTo = [[None for _ in range(w)] for _ in range(h)]

        for i in range(w):
            distTo[0][i] = self.MAX_ENERGY

        for y in range(1, h):
            for x in range(0, w):
                min_index, min_value = x, distTo[y - 1][x]

                if (x > 0) and (min_value > distTo[y - 1][x - 1]):
                    min_index = x - 1
                    min_value = distTo[y - 1][x - 1]

                if (x < w - 1) and (min_value > distTo[y - 1][x + 1]):
                    min_index = x + 1
                    min_value = distTo[y - 1][x + 1]
                
                distTo[y][x] = min_value + self.energy(x, y)
                edgeTo[y][x] = min_index


        result = [-1] * h
        min_x, min_value = -1, self.MAX_ENERGY * h

        for z in range(0, w):
            if distTo[h - 1][z] < min_value:
                min_x = z
                min_value = distTo[h - 1][z]

        for y in range(h - 1, -1, -1):
            result[y] = min_x
            min_x = edgeTo[y][min_x]
            
        return result


def showBeforeAfterSeamCarving(fileName, numCarve):
    image = Image.open(Path(__file__).with_name(fileName)) # Use the location of the current .py file
    assert(numCarve <= image.size[0])
    assert(image.size[0] <= 100 and image.size[1] <= 100)
    sc = SeamCarver(image)
    for i in range(numCarve): sc.removeVerticalSeam(sc.findVerticalSeam())                                  
    
    image = image.resize((image.size[0]*10, image.size[1]*10))    
    sc.image = sc.image.resize((sc.image.size[0]*10, sc.image.size[1]*10))

    # Concatenate two images side-by-side
    concat = Image.new("RGB", (image.size[0]+sc.image.size[0]+1, image.size[1]), "black")
    concat.paste(image, (0,0))
    concat.paste(sc.image, (image.size[0]+1, 0))
    concat.show()
    

'''
    Iterate over pixels and change colors to gray scale
'''
def convertToGrayScale(image):
    assert(isinstance(image, Image.Image))
    image2 = Image.new(mode="RGB", size=(image.size[0],image.size[1]), color='white') # Create a new white image of the same size
    pixels1 = image.load() # Get pixel map
    pixels2 = image2.load()
    for col in range(image.size[0]): # width
        for row in range(image.size[1]): # height
            r,g,b = pixels1[col,row]
            y = int(0.299*r + 0.587*g + 0.144*b) # Change color to gray scale
            pixels2[col,row] = (y,y,y)
    return image2


if __name__ == "__main__":        
    '''
    # Unit test for convertToGrayScale()    
    image_color = Image.open(Path(__file__).with_name("heart.jpg")) # Use the location of the current .py file    
    image_gray = convertToGrayScale(image_color)
    image_color.show()
    image_gray.show()
    '''    

    
    # Unit test 1 for vertical seam    
    image = Image.new("RGB", (10,10), "white")
    pixels = image.load()
    for row in range(image.size[0]):         
        pixels[4,row] = (255,0,0)
        pixels[5,row] = (255,0,0)
    sc = SeamCarver(image)           
    #print(sc.energeMap(), '\n')
    #sc.image.show()
    
    vs = sc.findVerticalSeam()
    print(sc.energyMapWithVerticalSeam(vs),'\n')
    if int(sc.energySumOverVerticalSeam(vs)) == 2000: print("pass")
    else: print("fail")
    sc.removeVerticalSeam(vs)
    # sc.width() == 9    
    
    vs = sc.findVerticalSeam()
    #print(sc.energyMapWithVerticalSeam(vs),'\n')  
    if int(sc.energySumOverVerticalSeam(vs)) == 2000: print("pass")
    else: print("fail")
    sc.removeVerticalSeam(vs)
    # sc.width() == 8

    vs = sc.findVerticalSeam()
    #print(sc.energyMapWithVerticalSeam(vs),'\n')
    if int(sc.energySumOverVerticalSeam(vs)) == 2000: print("pass")
    else: print("fail")
    sc.removeVerticalSeam(vs)
    # sc.width() == 7

    vs = sc.findVerticalSeam()
    #print(sc.energyMapWithVerticalSeam(vs),'\n')
    if int(sc.energySumOverVerticalSeam(vs)) == 2000: print("pass")
    else: print("fail")
    sc.removeVerticalSeam(vs)
    # sc.width() == 6

    vs = sc.findVerticalSeam()
    #print(sc.energyMapWithVerticalSeam(vs),'\n')
    if int(sc.energySumOverVerticalSeam(vs)) == 4880: print("pass")
    else: print("fail")
    sc.removeVerticalSeam(vs)
    # sc.width() == 5

    
    # Unit test 2 for vertical seam
    image2 = Image.new("RGB", (3,10), "white")
    sc2 = SeamCarver(image2)
    vs2 = sc2.findVerticalSeam()
    print(sc2.energyMapWithVerticalSeam(vs2))
    if all([vs2[i]==1 for i in range(1,image2.size[0]-1)]): print("pass")
    else: print("fail")
    sc2.removeVerticalSeam(vs2)
    # sc2.width() == 2

    image3 = Image.open(Path(__file__).with_name("heart.jpg")) # Use the location of the current .py file
    sc3 = SeamCarver(image3)
    vs3 = sc3.findVerticalSeam()
    if int(sc3.energySumOverVerticalSeam(vs3)) == 2000: print("pass")
    else: print("fail")
    
    image3 = Image.open(Path(__file__).with_name("stars.jpg")) # Use the location of the current .py file
    sc3 = SeamCarver(image3)        
    vs3 = sc3.findVerticalSeam()      
    if int(sc3.energySumOverVerticalSeam(vs3)) == 2000: print("pass")
    else: print("fail")        

    image3 = Image.open(Path(__file__).with_name("piplub.jpg")) # Use the location of the current .py file
    sc3 = SeamCarver(image3)
    vs3 = sc3.findVerticalSeam()
    if int(sc3.energySumOverVerticalSeam(vs3)) == 2000: print("pass")
    else: print("fail")
    
    
    # Unit test 3: visual inpsection for seam carving
    showBeforeAfterSeamCarving("heart.jpg", 30)    # carving 후에 흰 부분만 삭제되고 하트 부분은 유지되어야 함    
    showBeforeAfterSeamCarving("stars.jpg", 20)    # 별 3개 모양 carving 전후에 유지되어야 함
    showBeforeAfterSeamCarving("piplub.jpg", 30)   # carving 후에 흰 부분만 삭제되고 piplub은 유지되어야 함

    
    # Speed test (effective only when you pass the accuracy test)
    image3 = Image.open(Path(__file__).with_name("piplub.jpg")) # Use the location of the current .py file
    sc3 = SeamCarver(image3)
    n=20
    tVerticalSeam = timeit.timeit(lambda: sc3.findVerticalSeam(), number=n)/n
    tGrayScale = timeit.timeit(lambda: convertToGrayScale(image3), number=n)/n
    print(f"Finding {n} vertical seams on a 100x100 image took {tVerticalSeam:.10f} sec on average")
    print(f"Creating {n} gray scale images on a 100x100 image took {tGrayScale:.10f} sec on average")    
    if (tVerticalSeam < 12 * tGrayScale): print("pass for speed test")
    else: print("fail for speed test")
    
    