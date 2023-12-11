

# Declare lists of x coords and y coords
x = []
y = []

maxVal = 0

# This is used to know when a value is at max relative intensity for the spectrometer
# This means we don't know if the peak actually goes higher or not since the spectrometer is oversaturated
spectrometerMax = 0.95

# Open file, skip metadata

print("Oversaturated peaks:", end = " ")

with open('Near Sun.txt') as f:
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
# count as a peak or dip by the program

# If you only want to detect for one of these then increase the noise difference number to 1 for the one you don't want detected.
noiseDifEmission = 0.0009
noiseDifAbsorption = 0.0009

# Number of digits to round to for each intensity coordinate
digits = 4



xListE = []
yListE = []

xListA = []
yListA = []

formatter = '{:.' + '{}'.format(digits) + 'f}'

print("\n")
print("Inaccurate peaks:", end = "\n\n")

# Find peaks
noiseDif = noiseDifEmission
 
count = 1
while count < len(y)-1 :
    
    leftDif = y[count]-y[count-1]
    rightDif = y[count]-y[count+1]
    

    if leftDif > noiseDif and rightDif > noiseDif :
        yListE.append(y[count])
        xListE.append(x[count])
        
    # This elif checks to see if either the left point difference or right point difference satisfies the noiseDif but
    # not both of them. Some peaks were inaccurate because they had two points close together at the top of the peak.
    # This might happen since the actual peak was right between the two points.
    elif (leftDif > noiseDif or rightDif > noiseDif) :
        if(leftDif >= 0 and rightDif >= 0) :
            print("    " + str(x[count]) + " & " + str(formatter.format(y[count])) + "\\\\")

    count += 1

# Print results
print("\n", end = "")
print("Well defined emission lines determined by noise threshold:", end = "\n\n")

count = 0
while count < len(yListE) :
    
    print("    " + str(xListE[count]) + " & " + str(formatter.format(yListE[count])) + "\\\\")
    
    count += 1

print("\n", end = "")
print("Inaccurate dips:", end = "\n\n")
# Find dips
noiseDif = noiseDifAbsorption

count = 1
while count < len(y)-1 :
    
    dipLen = 0
    
    leftDif = y[count-1]-y[count]
    rightDif = y[count+1]-y[count]
    
    dipLen = (leftDif + rightDif) / 2

    if leftDif > noiseDif and rightDif > noiseDif :
        yListA.append(dipLen)
        xListA.append(x[count])
        
        
    elif (leftDif > noiseDif or rightDif > noiseDif) :
        if(leftDif >= 0 and rightDif >= 0) :
            print("    " + str(x[count]) + " & " + str(formatter.format(dipLen)) + "\\\\")

    count += 1

# Print results
print("\n", end = "")
print("Absorption dips are measured by the average change in intensity between the dip point and the two adjacent points")
print("Well defined absorption dips determined by noise threshold:", end = "\n\n")

count = 0
while count < len(yListA) :
    
    print("    " + str(xListA[count]) + " & " + str(formatter.format(yListA[count])) + "\\\\")
    
    count += 1

    
    