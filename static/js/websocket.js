$(function () {
	let conn = null;
	let reconncect = null;

	function connect() {
		disconnect();
		let wsUri = (window.location.protocol === 'https:' && 'wss://' || 'ws://') + window.location.host;
		conn = new WebSocket(wsUri);

		console.log(`Connecting to ${wsUri}...`);

		conn.onopen = function () {
			console.log('Connected!');
			clearInterval(reconncect);
			update_ui();
		};

		conn.onmessage = function (e) {
			$("#info").html(e.data.trim());
		};

		conn.onclose = function () {
			console.log('Dropped!');
			conn = null;
			update_ui();
			reconncect = window.setInterval(connect, 10000);
		};
	}

	function disconnect() {
		if (conn !== null) {
			conn.close();
			conn = null;
			update_ui();
		}
	}

	function update_ui() {
		const text = conn === null ? 'disconnected' : 'connected';
		$('#status').text(text);
	}

	connect();

});
