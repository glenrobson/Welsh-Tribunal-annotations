% import index
<%
    if grounds == 'missing_grounds':
        groundsText = 'Missing grounds'
        grounds = ''
    else:
        groundsText = grounds
    end
%>
<html>
    <head>
    <title>Grounds - {{ groundsText }}</title>
    </head>
    <body>
        <h1>Applicants who appled with the grounds: {{ reasons[grounds] }}</h1>
        <a href="index.html">Back to summary</a>
        <ul>
            % for year in keyOrders['year']:
                <% if year == '':
                    year = 'Date not listed'
                    link = 'no_year'
                else:
                    link = year
                end %>
                <li><a href="#{{link}}">{{year}}</a></li>
            % end    
        </ul>
        % for year in keyOrders['year']:
             <% if year == '':
                    year_text = 'Date not listed'
                    link = 'no_year'
                else:
                    year_text = year
                    link = year
                end %>

            <h2><a name="{{ link }}">{{ year_text }}</a></h2>
            <hr/>
            % if year in data:
                % for applicant in data[year]:
                    <p>
                        <p><b>{{ index.printIfAvliable('Name', applicant['metadata']) }}</b>, {{ index.printIfAvliable('Age', applicant['metadata']) }}, {{ index.printIfAvliable('Occupation, profession or business', applicant['metadata']) }} </p>
                        <p><b>Grounds:</b>
                        <ul>
                            % for ground in applicant['ground'].split(' '):
                                <li>({{ ground.lower() }}) - {{ reasons[ground] }} </li>
                            % end
                        </ul>
                        <p><b>Reasons: </b> {{index.printIfAvliable('Reasons', applicant['metadata']) }} </p>
                        <p><b>Verdict: </b> {{ index.printIfAvliable('Decision of the Tribunal', applicant['metadata']) }} </p>
                        <p><a href="http://iiif.gdmrdigital.com/ww1-tribunal/viewImage.html?manifest={{ applicant['images']['manifest'] }}&canvas={{ applicant['images']['canvas'] }} ">View Application</a>

                    </p>
                    <hr/>
                % end
            % end
        % end
    </body>
</html>    
