<html>
    <head>
    <title>Grounds</title>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['bar']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Date', 'Habitual national interest work', 'Wishes national interest work','Underaking education or trainnig','Hardship','Ill Health','Conscientious objector','Listed as a protected ocupation', 'Missing grounds'],
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
        <p>This is a visulisaiton of the National Library of Wales <a href="https://crowd.library.wales/en/s/war-tribunal-records/page/about">Cardiganshire War Tribunal records</a>. Code for this project is aviliable on <a href="https://github.com/glenrobson/Welsh-Tribunal-annotations">github</a>.</p>
        
        <p>It was possible to apply for exception from military service due to the following reasons:</p>
        <ul>
            <li>On the ground that it is expedient in the national interest that the man should instead of being employed in military service be engaged in other work in which is habitually engaged</li>
            <li>On the ground that it is expedient in the national interest that the man should instead of being employed in military service be engaged in other work in which he wishes to be engaged</li>
            <li>Trained or educated for a reserved occupation</li>
            <li>serious hardship</li>
            <li>ill health</li>
            <li>conscientious objection </li>
            <li>Listed as a protected ocupation</li>
        </ul>    
        <p>This page looks at the different reasons grouped by year of application. Due to time constraints it is limited to the Aberystwyth Borough District and the 'Beige R41/42' form.</p>
        <div id="barchart_material" style="width: 900px; height: 500px;"></div>
            <h2>1916</h2>
            <ul>
                % key = '1916'
                <li>{{ data[key]['A']}} - Habitual national interest work</li>
                <li>{{ data[key]['B']}} - Wishes national interest work</li>
                <li>{{ data[key]['C']}} - Underaking education or trainnig</li>
                <li>{{ data[key]['D']}} - Hardship</li>
                <li>{{ data[key]['E']}} - Ill Health</li>
                <li>{{ data[key]['F']}} - Conscientious objector</li>
                <li>{{ data[key]['G']}} - Listed as a protected ocupation</li>
                <li>{{ data[key]['']}} - Missing grounds</li>
            </ul>
            <h2>1917</h2>
            <ul>
                % key = '1917'
                <li>{{ data[key]['A']}} - Habitual national interest work</li>
                <li>{{ data[key]['B']}} - Wishes national interest work</li>
                <li>{{ data[key]['C']}} - Underaking education or trainnig</li>
                <li>{{ data[key]['D']}} - Hardship</li>
                <li>{{ data[key]['E']}} - Ill Health</li>
                <li>{{ data[key]['F']}} - Conscientious objector</li>
                <li>{{ data[key]['G']}} - Listed as a protected ocupation</li>
                <li>{{ data[key]['']}} - Missing grounds</li>
            </ul>
            <h2>1918</h2>
            <ul>
                % key = '1918'
                <li>{{ data[key]['A']}} - Habitual national interest work</li>
                <li>{{ data[key]['B']}} - Wishes national interest work</li>
                <li>{{ data[key]['C']}} - Underaking education or trainnig</li>
                <li>{{ data[key]['D']}} - Hardship</li>
                <li>{{ data[key]['E']}} - Ill Health</li>
                <li>{{ data[key]['F']}} - Conscientious objector</li>
                <li>{{ data[key]['G']}} - Listed as a protected ocupation</li>
                <li>{{ data[key]['']}} - Missing grounds</li>
            </ul>
            <h2>Date not listed</h2>
            <ul>
                % key = ''
                <li>{{ data[key]['A']}} - Habitual national interest work</li>
                <li>{{ data[key]['B']}} - Wishes national interest work</li>
                <li>{{ data[key]['C']}} - Underaking education or trainnig</li>
                <li>{{ data[key]['D']}} - Hardship</li>
                <li>{{ data[key]['E']}} - Ill Health</li>
                <li>{{ data[key]['F']}} - Conscientious objector</li>
                <li>{{ data[key]['G']}} - Listed as a protected ocupation</li>
                <li>{{ data[key]['']}} - Missing grounds</li>
            </ul>
        % end
    </body>
</html>    
