class FileParser:

    def __init__(self):
        self._fileName = "IDs.txt"
        self.readData = []
        self.Read()
    
    def Read(self):
        with open(self._fileName, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) >= 4:
                    ID = parts[0]
                    xCoord = float(parts[1])
                    yCoord = float(parts[2])
                    description = ' '.join(parts[3:])

                    self.readData.append({
                    'ID': ID,
                    'xCoord': xCoord,
                    'yCoord': yCoord,
                    'description': description
                })

    def Write(self,id:int, xCoord:int, yCoord:int, desc:str):
        with open(self._fileName, 'w') as file:
            line = f"{id} {xCoord} {yCoord} {desc}\n"
            file.write(line)