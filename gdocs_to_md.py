import pandas as pd
from datetime import datetime, date

def date_range_string(start, end):
	start = str(start)
	end = str(end)
	month = ['', 'January','February','March','April','May','June','July','August','September','October','November','December']
	start = [month[int(start[4:6])],int(start[6:]),int(start[:4])]
	end =   [month[int(  end[4:6])],int(  end[6:]),int(  end[:4])]

	if start[0] == end[0]:
		end[0] = ''

	if start[2] == end[2]:
		start[2] = ''

	left = ' '.join(map(str,start)).replace('  ',' ')

	right = ' '.join(map(str,end)).replace('  ',' ')

	return left+' - '+right


def date_and_place(start,end,location):
	return f"<span class = 'date_and_place'>({date_range_string(start, end)}, {location})</span>"


def application_deadline(deadline):
	try:
		deadline = datetime.strptime(str(int(deadline)), '%Y%m%d')


		if deadline<datetime.now():
			return "<span class = 'application over'> Applications over</span>"

		else:
			return f"<span class = 'application due'> Applications due {deadline.strftime('%B %d, %Y')}</span>"

	except ValueError:
		return ""


def format_conference(Title,URL,Date_Start,Date_End,Location,Description, App_Deadline, **kwargs):

	return f'''## [{Title}]({URL})
{date_and_place(Date_Start,Date_End,Location)} {application_deadline(App_Deadline)}


'''


sheet_id = "1_HQcll_r8Rj39uZ1GN-tfrgHLurwSsfShlBZjMlYfuE"
sheet_names = ("Summer_Schools","Conferences", "Long_Programs")
titles = ("Summer Schools", "Conferences", "Long Programs")


head = """
<style>
  .application{
  font-style: italic;
  }
  .application.over{
  color:#bb2222;
  }
  .date_and_place{
  }
  
  h2{
  margin-bottom:5px
  }
</style>
"""

with open('index.md', 'w') as f:
	f.write(head)
	for title, sheet_name in zip(titles, sheet_names):
		url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
		schools = pd.read_csv(url)
		f.write(f'## {title}\n\n')
		for row in schools.to_dict(orient="records"):
			f.write(format_conference(**row))

		f.write("___\n")