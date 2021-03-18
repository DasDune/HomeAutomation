var term;
var ws;
var connected = false;
var binary_state = 0;
var put_file_name = null;
var put_file_data = null;
var get_file_name = null;
// id = 111;
// var url = `ws://192.168.1.${id}:8266/`
var get_file_data = null;

cmdEle = document.getElementById(`cmd`);
brkEle = document.getElementById(`brk`);
clrEle = document.getElementById(`clr`);
ctrlEle = document.getElementById(`ctrl`);
filesEle = document.getElementById(`files`);
resetEle = document.getElementById(`reset`);

out01 = document.getElementById(`out-0-1`);
out11 = document.getElementById(`out-1-1`);
out21 = document.getElementById(`out-2-1`);
out31 = document.getElementById(`out-3-1`);
out00 = document.getElementById(`out-0-0`);
out10 = document.getElementById(`out-1-0`);
out20 = document.getElementById(`out-2-0`);
out30 = document.getElementById(`out-3-0`);

term = document.getElementById(`term`);
term.className = `term`;
term.rows = "10";
term.cols = "50";

key = (e) => {
    if (e.ctrlKey) alert(`The ctrl key is pressed`);
    if (e.key == "Enter") ws.send(`${cmd.value}\r`);
}

brk = () => {
    ws.send(`\x03`);
}

clr = () => {
    term.value = '';
}

ctrl = () => {
    console.log(ctrlEle.value);
    url = `ws://192.168.1.${ctrlEle.value}:8266/`
    connect(url);
}

files = () => {
    ws.send(`os.listdir()\r`);
}

reset = () => {
    ws.send(`import machine\r`);
    ws.send(`machine.reset()\r`);
}

out = (e) => {

    addr = e.target.id.split("-")[1];
    cmd = e.target.id.split("-")[2];
    ws.send(`O${addr}.value(${cmd})\r`);

}


cmdEle.addEventListener("keydown", key);
brkEle.addEventListener("click", brk);
clrEle.addEventListener("click", clr);
ctrlEle.addEventListener("change", ctrl);
filesEle.addEventListener("click", files);
resetEle.addEventListener("click", reset);

out01.addEventListener("click", out);
out11.addEventListener("click", out);
out21.addEventListener("click", out);
out31.addEventListener("click", out);
out00.addEventListener("click", out);
out10.addEventListener("click", out);
out20.addEventListener("click", out);
out30.addEventListener("click", out);


connect = (url) => {
    if (ws) ws.close();
    ws = new WebSocket(url);
    ws.binaryType = 'arraybuffer';

    ws.onopen = () => {
        term.value = `Welcome to Controller C${ctrlEle.value}!`;
        ws.onmessage = (e) => {
            if (e.data.match(/Password/)) ws.send(`Benoit\r`);
            // else term.write(e.data);
            else term.value += e.data;
            console.log(e.data);
        }
    };
};



