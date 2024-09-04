html = """
<!DOCTYPE html>
<html>
	<head>
	
		<meta charset="UTF-8">

<title>Lake Riders Club</title>

<meta name="description" xml:lang="fr" content="Lake Riders Club, club dédié au sport nautique sur le lac Léman" lang="fr" />
<meta name="keywords" xml:lang="fr" content="wakeboards, wakesurf, wakeskate, Sport nautique, Lac Léman, Genève, Suisse, Lake Riders Club" lang="fr" />

<meta name="viewport" content="initial-scale=1.0" />

<link rel="shortcut icon" href="/favicon.ico" />	
<link rel="stylesheet" href="/css/styles.css" media="all" />
<link rel="stylesheet" href="/js/fancybox/jquery.fancybox.css" type="text/css" media="screen" />
<link rel="stylesheet" href="/js/fancybox/jquery.fancybox-thumbs.css" type="text/css" media="screen" />


<script type="text/javascript" src="/js/jquery-1.11.2.min.js"></script>
<script type="text/javascript" src="/js/jquery-migrate-1.2.1.min.js"></script>
<script type="text/javascript" src="/js/jquery.easing.1.3.js"></script>
<script type="text/javascript" src="/js/jquery-validate/jquery.validate.js"></script>
<script type="text/javascript" src="/js/jquery-validate/methods.js"></script>
<script type="text/javascript" src="/js/jquery-validate/localization/messages_fr.js"></script>
<script type="text/javascript" src="/js/jquery.placeholder.js"></script>
<script type="text/javascript" src="/js/fancybox/jquery.fancybox.js"></script>
<script type="text/javascript" src="/js/fancybox/jquery.fancybox-thumbs.js"></script>
<script type="text/javascript" src="/js/fancybox/jquery.fancybox-media.js"></script>
<script type="text/javascript" src="/js/jquery.parallax-scroll.js"></script>
<script type="text/javascript" src="/js/communs.js"></script>

<script>
	
	var dateNow = "2024-08-31";
	

	$(document).ready(function() {
		
		function renderCalendar() {
			$('#calendar').fullCalendar({
				header: {
					left: 'prev,next today',
					center: 'title',
					right: 'basicWeek,basicDay'
				},
				defaultDate: dateNow,
				defaultView: 'basicWeek',
				lang: 'fr',
				height: 'auto',
				minTime: '18:00:00',
				maxTime:'21:00:00',
				allDaySlot: false,
				buttonIcons: true, // show the prev/next text
				weekNumbers: false,
				editable: false,
				eventLimit: false, // allow "more" link when too many events
				timeFormat: 'H:mm',
				slotEventOverlap: false,
				weekends: false,
                                viewRender: function(currentView){
                                    var minDate = moment();
                                    if (minDate >= currentView.start && minDate <= currentView.end) {
                                        $(".fc-prev-button").prop('disabled', true); 
                                        $(".fc-prev-button").addClass('fc-state-disabled'); 
                                    }
                                    else {
                                        $(".fc-prev-button").removeClass('fc-state-disabled'); 
                                        $(".fc-prev-button").prop('disabled', false); 
                                    }

                                },
				events: [
																				{
						title: ' ',
						start: '2024-06-03T18:00:00',
						end: '2024-06-03T19:00:00',
												color: '#D3D3D3',
						description: 'Reservé par  '
											},
																				{
						title: 'Legolas L.',
						start: '2024-06-03T18:00:00',
						end: '2024-06-03T19:00:00',
												color: '#D3D3D3',
						description: 'Reservé par Legolas L.'
											},
																				{
						title: 'Gimli G.',
						start: '2024-06-03T18:00:00',
						end: '2024-06-03T19:00:00',
												color: '#D3D3D3',
						description: 'Reservé par Gimli G.'
											},
																				{
						title: 'Aragorn A.',
						start: '2024-06-03T18:00:00',
						end: '2024-06-03T19:00:00',
												color: '#D3D3D3',
						description: 'Reservé par Aragorn A.'
											},
																														{
						title: 'Gandalf G.',
						start: '2024-06-03T19:00:00',
						end: '2024-06-03T20:00:00',
												color: '#D3D3D3',
						description: 'Reservé par Gandalf G.'
											},
																				{
                        title: 'Place disponible',
												color: '#82BCF3',
												url: '?reserver=44036',
						start: '2024-06-03T19:00:00',
						end: '2024-06-03T20:00:00',
						description: 'Cliquez pour réserver entre 19:00 et 20:00'
											},
																				{
						title: 'Sam S.',
						start: '2024-06-03T19:00:00',
						end: '2024-06-03T20:00:00',
												color: '#D3D3D3',
						description: 'Reservé par Sam S.'
											},
																				{
                        title: 'Place disponible',
												color: '#82BCF3',
												url: '?reserver=44036',
						start: '2024-06-03T19:00:00',
						end: '2024-06-03T20:00:00',
						description: 'Cliquez pour réserver entre 19:00 et 20:00'
											},
																														{
						title: 'Frodo F.',
						start: '2024-06-03T20:00:00',
						end: '2024-06-03T21:00:00',
												color: '#D3D3D3',
						description: 'Reservé par Frodo F.'
											},
																				{
						title: 'Place disponible',
												color: '#82BCF3',
												url: '?reserver=44036',
						start: '2024-06-03T20:00:00',
						end: '2024-06-03T21:00:00',
						description: 'Cliquez pour réserver entre 20:00 et 21:00'
											},
																				{
						title: 'Session annulée',
						color: '#BF0000',
						start: '2024-06-03T20:00:00',
						end: '2024-06-03T21:00:00',
						description: 'La session est annulée.'
											},
																				{
						title: 'Session annulée',
						color: '#BF0000',
						start: '2024-06-03T20:00:00',
						end: '2024-06-03T21:00:00',
						description: 'La session est annulée.'
											},
																														]
				eventRender: function(event, element) {
					element.qtip({
						content: event.description,
						 position: {
							 target: 'mouse', // Track the mouse as the positioning target
							 adjust: { x: 5, y: 5 } // Offset it slightly from under the mouse
						 }
					});
				}
			});
		}

		renderCalendar();
	});

</script>
</footer>			
			<a href="#" id="btn_up">
				<img alt="Retour" title="Retour" src="/images/communs/top.png" />
			</a>
			
	</body>
</html>						
"""

calendar_entries_dict = {
    "2024-06-03T18:00:00": "EMPTY,Legolas L.,Gimli G.,Aragorn A.",
    "2024-06-03T19:00:00": "Gandalf G.,FREE,Sam S.,FREE",
    "2024-06-03T20:00:00": "Frodo F.,FREE,CANCELLED,CANCELLED",
}
