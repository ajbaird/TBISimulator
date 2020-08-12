class DataPoint:
    """Stores association and VEGF growth scaling factors, the volume regrown, and number of bisecting and sprouting nodes"""

    def __init__(self, vScale, aScale, volumeGrowth, numBisecting, numSproutNodes):
        self.vScale = vScale
        self.aScale = aScale
        self.volumeGrowth = volumeGrowth
        self.numBisecting = numBisecting
        self.numSprouts = numSproutNodes

    def SetMaxVEGF(self, maxVEGF):
        self.maxVEGF = maxVEGF
    def SetMaxBound(self, maxBound):
        self.maxBound = maxBound

    def Print(self):
        print(f"A: {round(self.aScale, 1)}, V: {round(self.vScale, 1)}, "
              f"Volume growth: {round(self.volumeGrowth)}, "
              f"# Bisecting: {self.numBisecting}, # Sprouts: {self.numSprouts}")
