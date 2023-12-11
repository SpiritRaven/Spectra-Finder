

# Declare lists of x coords and y coords
x = []
y = []

maxVal = 0

# This is used to know when a value is at max relative intensity for the spectrometer
# This means we don't know if the peak actually goes higher or not since the spectrometer is oversaturated
spectrometerMax = 0.95

# Open file, skip metadata

print("Oversaturated peaks:", end = " ")

with open('Mercury.txt') as f:
    for i in range(7):
        next(f)
        
    for i in f:
        line = i.split()
        
        currentX = float(line[0])
        currentY = float(line[1])
    
        # Find if anything is oversaturated and declare it as oversaturated 
        if currentY > spectrometerMax :
            print(str(currentX), end = ", ")
    
        x.append(currentX)
        y.append(currentY)
        
        if currentY > maxVal :
            maxVal = currentY
        
   
f.close()


# Take every y coordinate and change it so that the data keeps its ratio and the max value is 1
intensityCorrection = 1/maxVal
count = 0

while count < len(y) :
    y[count] *= intensityCorrection

    count += 1


# Noise threshold, this value dictates how large a difference is needed between two points for it to 
# count as a peak by the program
noiseDif = 0.0009


count = 1

xList = []
yList = []

print("\n")

# Find peaks 
while count < len(y)-1 :
    
    leftDif = y[count]-y[count-1]
    rightDif = y[count]-y[count+1]
    

    if leftDif > noiseDif and rightDif > noiseDif :
        yList.append(y[count])
        xList.append(x[count])
        
    # This elif checks to see if either the left point difference or right point difference satisfies the noiseDif but
    # not both of them. Some peaks were inaccurate because they had two points close together at the top of the peak.
    # This might happen since the actual peak was right between the two points.
    elif (leftDif > noiseDif or rightDif > noiseDif) :
        if(leftDif >= 0 and rightDif >= 0) :
            print(str(x[count]) + " " + str(y[count]) + " Satisfies the condition for a peak but is inaccurate\n")

    count += 1
    
# Print results
count = 0
while count < len(yList) :
    
    print("    " + str(xList[count]) + " & " + str(round(yList[count],4)) + "\\\\")
    
    count += 1
    
    