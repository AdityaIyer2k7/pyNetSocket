print('The documentation for the pyNetSocket library')
print('This covers all the information you need to start')
print('')
print('Topics:',
      'server',
      'client',
      'callbacks',
      sep='\n\t')
print('To view information:',
      'import pyNetSocket.docs.TOPIC',
      sep='\n')
print('')
print('You can see the full guides here:')
print('https://github.com/DrSparky-2007/PyNetSocket/wiki/')
openLink = input('Open link in browser? (y/n) ')[0].lower()

if openLink == 'y':
  import webbrowser as wb
  wb.open('https://github.com/DrSparky-2007/PyNetSocket/wiki/')
