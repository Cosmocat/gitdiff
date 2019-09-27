import re

def parser(data):
    mlData = data.get('diff').splitlines()
    diffSegments = []
    parsedSegments = []
    currentSegment = ''

    for num, line in enumerate(mlData, start=1):
        if re.findall(r'diff --git*', line):
            if (currentSegment != ''):
                diffSegments.append(currentSegment)
                currentSegment = ''
        currentSegment = currentSegment + line + '\n'
        if (num == len(mlData)):
            diffSegments.append(currentSegment)

    for segment in diffSegments:
        splitSegment = segment.splitlines()
        if(splitSegment[2].startswith('Binary') or splitSegment[3].startswith('Binary')):
            parsedSegments.append({'header': 'Binary files differ'}) 
            continue
        chunkStart = 0 
        try:
            chunkStart = splitSegment.index(next(x for x in splitSegment if '@@' in x))
        except:
            parsedSegments.append({'header': 'Unable to find proper chunk descriptor'})
            continue

        chunks = splitIntoChunks(splitSegment[chunkStart:])
        apos = splitSegment[0].find('a/')
        bpos = splitSegment[0].find('b/')
        oldFilename = splitSegment[0][apos:bpos-1]
        newFilename = splitSegment[0][bpos:]

        segmentHeader = oldFilename[2:]
        segmentContent = []

        if(splitSegment[1].startswith('deleted')):
            segmentDiffType = 'deleted'
            for line in chunks[0]['content']:
                segmentContent.append({'linechangeInd': '-', 'lineContent': line[1:]})
        elif(splitSegment[1].startswith('new')):
            segmentDiffType = 'added'
            for line in chunks[0]['content']:
                segmentContent.append({'linechangeInd': '+', 'lineContent': line[1:]})
        elif(splitSegment[1].startswith('index')):
            segmentDiffType = 'modified'
            segmentContent = parseChunks(chunks)
        elif(splitSegment[1].startswith('similarity')):
            segmentDiffType = 'renamed'
            segmentHeader = oldFilename[2:] + '-->' + newFilename[2:]
            segmentContent = parseChunks(chunks)
        else:
            parsedSegments.append({'header': 'Unable to find proper diff type'})
            continue
        
        parsedSegments.append({'header': segmentHeader, 'type': segmentDiffType, 'content': segmentContent})

    return parsedSegments

# if diff segment has more than one chunk, split it into array of chunks
def splitIntoChunks(segment):
    chunks = []
    currentChunk = {'descriptor': '', 'content': []}
    for line in segment:
        if line.startswith('@@'):
            # if previous chunk exists append it and start new one
            if(currentChunk['descriptor'] != ''):
                chunks.append(currentChunk)
            currentChunk = {'descriptor': '', 'content': []}
            currentChunk['descriptor'] = line
        else:
            currentChunk['content'].append(line)

    # append current chunk before return
    chunks.append(currentChunk)
    return chunks

# parse descriptor to get starting lines
def parseDescriptor(descriptor):
    # removing @@
    descriptor = descriptor[2:]
    descriptor = descriptor[:-2]

    try:
        origDesc = descriptor.split(' ')[1].split(',')
        modifDesc = descriptor.split(' ')[2].split(',')
    except:
        return 'Unable to parse descriptor'
    return [int(origDesc[0][1:]), int(modifDesc[0][1:])]

# parse chunks of diff
def parseChunks(chunks):
    segmentContent = []
    for chunk in chunks:
        parsedDescriptor = parseDescriptor(chunk['descriptor'])
        if (isinstance(parsedDescriptor, str)):
            segmentContent.append({'error':'Unable to parse chunk descriptor'})
            continue
        for line in chunk['content']:
            if (line[:1] == '+'):
                segmentContent.append({'linechangeInd': '+', 'lineContent': line[1:], 'linenumNew': parsedDescriptor[1]})
            elif (line[:1] == '-'):
                segmentContent.append({'linechangeInd': '-', 'lineContent': line[1:], 'linenumOld': parsedDescriptor[0]})
            else:
                segmentContent.append({'lineContent': line, 'linenumNew': parsedDescriptor[1], 'linenumOld': parsedDescriptor[0]})
            parsedDescriptor[0] +=1
            parsedDescriptor[1] +=1
    return segmentContent