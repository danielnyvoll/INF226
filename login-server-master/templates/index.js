var reqId = 0;
var anchor = document.getElementById('anchor');
var searchField = document.getElementById('search');
var senderField = document.getElementById('sender');
var receiverField = document.getElementById('receiver')
var messageField = document.getElementById('message');
var searchBtn = document.getElementById('searchBtn');
var sendBtn = document.getElementById('sendBtn');
var allBtn = document.getElementById('allBtn');
var logOutBtn = document.getElementById('logoutBtn');
var output = document.getElementById('output');
var header = document.getElementById('header');
var csrftoken = document.getElementById('csrf_token').value


var checkAnnouncements = async () => {
    res = await fetch('/announcements');
    anns = await res.json();
    if (anns && Array.isArray(anns.data)) {
        const elts = [];
        anns.data.forEach((element, idx) => {
            if (idx > 0) {
                const node = document.createElement('li');
                node.textContent = '  …  ';
                elts.push(node);
            }
            const node = document.createElement('li');
            node.textContent = `${element.message || ''}`;
            elts.push(node);
        });
        header.replaceChildren(...elts);
    }
};
var search = async (query) => {
    const id = reqId++;
    const q = `/search?q=${encodeURIComponent(query)}`;
    res = await fetch(q);
    const body = document.createElement('p');
    body.innerHTML = await res.text();
    output.appendChild(body);
    body.scrollIntoView({block: "end", inline: "nearest", behavior: "smooth"});
    anchor.scrollIntoView();
    checkAnnouncements();
};
var send = async (sender, message, receiver) => {
    const id = reqId++;
    const q = `/send?sender=${encodeURIComponent(sender)}&message=${encodeURIComponent(message)}&receiver=${encodeURIComponent(receiver)}`;
    res = await fetch(q, { method: 'post', headers: {
        'X-CSRF-TOKEN': csrftoken
    } });
    const body = document.createElement('p');
    body.innerHTML = await res.text();
    output.appendChild(body); 
    body.scrollIntoView({block: "end", inline: "nearest", behavior: "smooth"});
    anchor.scrollIntoView();
    checkAnnouncements();
};

// Method for fetching logout function and restrict going back to app without being loged in
var logout = async () => {
    const id = reqId++;
    const q = 'logout'
    res = await fetch(q);
    location.reload()
}

searchField.addEventListener('keydown', ev => {
    if (ev.key === 'Enter') {
        search(searchField.value);
    }
});
searchBtn.addEventListener('click', () => search(searchField.value));
allBtn.addEventListener('click', () => search(senderField.value));
sendBtn.addEventListener('click', () => send(senderField.value, messageField.value, receiverField.value));
logoutBtn.addEventListener('click', () => logout())
checkAnnouncements();