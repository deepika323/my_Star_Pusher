def startScreen():
	titleRect = IMAGESDICT['title'].get_rect()
	topCoord = 50 
	titleRect.top = topCoord
	titleRect.centerx = HALF_WINWIDTH
	topCoord += titleRect.height
	
	instructionText = ['Push the stars over the marks.',
						'Arrow keys to move, WASD for camera control, P to change character.',
						'Backspace to reset level, Esc to quit.',
						'N for next level, B to go back a level.']

	DISPLAYSURF.fill(BGCOLOR)
	
	DISPLAYSURF.blit(IMAGESDICT['title'], titleRect)
	
	for i in range(len(instructionText)):
		instSurf = BASICFONT.render(instructionText[i], 1, TEXTCOLOR)
		instRect = instSurf.get_rect()
		topCoord += 10 
		instRect.top = topCoord
		instRect.centerx = HALF_WINWIDTH
		topCoord += instRect.height 
	DISPLAYSURF.blit(instSurf, instRect)

	while True: 
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					terminate()
				return
			
		pygame.display.update()
			FPSCLOCK.tick()	

def readLevelsFile(filename):
	assert os.path.exists(filename), 'Cannot find the level file: %s' % (filename)
	mapFile = open(filename, 'r')	
	content = mapFile.readlines() + ['\r\n']
	mapFile.close()

	levels = [] 
	levelNum = 0
	mapTextLines = []
	mapObj = [] 
	
	for lineNum in range(len(content)):
		line = content[lineNum].rstrip('\r\n')

		if ';' in line:
			line = line[:line.find(';')]
		if line != '':
			mapTextLines.append(line)
		elif line == '' and len(mapTextLines) > 0:
			maxWidth = -1
			for i in range(len(mapTextLines)):
				if len(mapTextLines[i]) > maxWidth:
					maxWidth = len(mapTextLines[i])
			for i in range(len(mapTextLines)):
				mapTextLines[i] += ' ' * (maxWidth - len(mapTextLines[i]))	
			for x in range(len(mapTextLines[0])):
				mapObj.append([])
			for y in range(len(mapTextLines)):
				for x in range(maxWidth):
					mapObj[x].append(mapTextLines[y][x])
			
			startx = None 
			starty = None
			goals = [] 
			stars = [] 
			for x in range(maxWidth):
				for y in range(len(mapObj[x])):
					if mapObj[x][y] in ('@', '+'):

						startx = x
						starty = y
					if mapObj[x][y] in ('.', '+', '*'):

						goals.append((x, y))
					if mapObj[x][y] in ('$', '*'):

						stars.append((x, y))
						
			assert startx != None and starty != None, 'Level %s (around line %s) in %s is missing a "@" or "+" to mark the start point.' % (levelNum+1, lineNum, filename)
			assert len(goals) > 0, 'Level %s (around line %s) in %s must have at least one goal.' % (levelNum+1, lineNum, filename)
			assert len(stars) >= len(goals), 'Level %s (around line %s) in %s is impossible to solve. It has %s goals but only %s stars.' % (levelNum+1, lineNum, filename, len(goals), len(stars))
			
			
			gameStateObj = {'player': (startx, starty),
			'stepCounter': 0,
			'stars': stars}
			
			
			levelObj = {'width': maxWidth,
			'height': len(mapObj),
			'mapObj': mapObj,
			'goals': goals,
			'startState': gameStateObj}

			
			levels.append(levelObj)
			
			mapTextLines = []
			mapObj = []
			gameStateObj = {}
			levelNum += 1
	return levels
	
	
def floodFill(mapObj, x, y, oldCharacter, newCharacter):

	if mapObj[x][y] == oldCharacter:
		mapObj[x][y] = newCharacter

	if x < len(mapObj) - 1 and mapObj[x+1][y] == oldCharacter:
		floodFill(mapObj, x+1, y, oldCharacter, newCharacter) 
	if x > 0 and mapObj[x-1][y] == oldCharacter:
		floodFill(mapObj, x-1, y, oldCharacter, newCharacter) 
	if y < len(mapObj[x]) - 1 and mapObj[x][y+1] == oldCharacter:
		floodFill(mapObj, x, y+1, oldCharacter, newCharacter) 
	if y > 0 and mapObj[x][y-1] == oldCharacter:
		floodFill(mapObj, x, y-1, oldCharacter, newCharacter)