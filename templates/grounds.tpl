<html>
    <head>
    <title>Grounds</title>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['bar']});
      google.charts.setOnLoadCallback(drawChart);
      <%
        titles = "'Date'"
        for ground in keyOrders['grounds']:
            titles += ", '{}'".format(reasons[ground]) 
        end    
      %>
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          [{{! titles }}],
          ['1916', {{ data['1916']['A'] }}, {{ data['1916']['B'] }}, {{ data['1916']['C'] }}, {{ data['1916']['D'] }}, {{ data['1916']['E'] }}, {{ data['1916']['F'] }}, {{ data['1916']['G'] }}, {{ data['1916'][''] }}],
          ['1917', {{ data['1917']['A'] }}, {{ data['1917']['B'] }}, {{ data['1917']['C'] }}, {{ data['1917']['D'] }}, {{ data['1917']['E'] }}, {{ data['1917']['F'] }}, {{ data['1917']['G'] }}, {{ data['1917'][''] }}],
          ['1918', {{ data['1918']['A'] }}, {{ data['1918']['B'] }}, {{ data['1918']['C'] }}, {{ data['1918']['D'] }}, {{ data['1918']['E'] }}, {{ data['1918']['F'] }}, {{ data['1918']['G'] }}, {{ data['1918'][''] }}],
          ['Date not listed', {{ data['']['A'] }}, {{ data['']['B'] }}, {{ data['']['C'] }}, {{ data['']['D'] }}, {{ data['']['E'] }}, {{ data['']['F'] }}, {{ data['']['G'] }}, {{ data[''][''] }}]
        ]);

        var options = {
          chart: {
            title: 'Reasons for exemption'
          },
          bars: 'veritcal' // Required for Material Bar Charts.
        };

        var chart = new google.charts.Bar(document.getElementById('barchart_material'));

        chart.draw(data, google.charts.Bar.convertOptions(options));
      }
    </script>
    
    </head>
    <body>
        <h1>Grounds for appeal by year</h1>
        <p>This is a visualisation of the National Library of Wales <a href="https://crowd.library.wales/en/s/war-tribunal-records/page/about">Cardiganshire War Tribunal records</a>. Code for this project is available on <a href="https://github.com/glenrobson/Welsh-Tribunal-annotations">github</a>.</p>
        
        <p>It was possible to apply for exception from military service for the following reasons:</p>
        <img src="https://damsssl.llgc.org.uk/iiif/2.0/image/4003522/549,4048,2571,817/1000,/0/default.jpg" />
           
        <p>This page looks at the different reasons for applying for an exemption grouped by year of application. Due to time constraints it is limited to the Aberystwyth Borough District and the 'Beige R41/42' form. Scroll down to see more information on the applicants.</p>
        <div id="barchart_material" style="width: 900px; height: 500px;"></div>
        <h1><a name="details">Applicant Details</a></h1>
        % for year in keyOrders['year']:
             <% if year == '':
                year_text = 'Date not listed'
                link = 'no_year'
            else:
                year_text = year
                link = year
            end %>
            <h2>{{ year_text }}</h2>
            <ul>
                % for ground in keyOrders['grounds']:
                    <%
                        if ground == '':
                            groundLink = 'missing_grounds'
                        else:
                            groundLink = ground
                        end
                    %>    
                
                    <li><a href="{{groundLink}}.html#{{link}}">{{ data[year][ground]}} - {{ reasons[ground]}}</a></li>
                % end
            </ul>
        % end
    </body>
</html>    
