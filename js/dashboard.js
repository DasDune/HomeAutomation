//Append the link to the style sheet to the html caller (index.html)
let link1 = document.createElement('link');
link1.href = 'http://DuneWebServer/projects/HomeAutomation/css/dashboard.css';
// link1.href = './doc.css';
link1.rel = 'stylesheet';
document.head.appendChild(link1);

//Append the link to fontawesome to the html caller (index.html)
let link2 = document.createElement('link');
link2.href = 'https://use.fontawesome.com/releases/v5.0.7/css/all.css';
link2.rel = 'stylesheet';
document.head.appendChild(link2);

// Import the database scripts
import { dbOp } from 'http://DuneWebServer/Dune/Lib/db.js';

// // Import the dom scripts
import { domOp } from 'http://DuneWebServer/Dune/Lib/dom.js';

//**Global var */

//*DB Tag object
let dbTag = {
  Description: null,
  IOType: null,
  Name: null,
  Node: null,
  PinNo: null,
  PinTag: null,
  PinType: null,
  Schedule: null
};

//DB change dispatcher
const dbChg = data => {
  let ele = {};
  switch (data.type) {
    case 'added':
      popTag(data.id, data.doc);
      break;

    case 'modified':
      ele = domOp({ id: `${data.id}-tag` });
      ele.parentNode.removeChild(ele);
      popTag(data.id, data.doc);
      break;

    case 'removed':
      ele = domOp({ id: `${data.id}-tag` });
      ele.parentNode.removeChild(ele);
      break;
  }
};

//Custom event listener for an empty DB Collection after a 'get' request, return the collection requested
document.addEventListener('colEmpty', e =>
  console.log('Cannot find the collection...')
);

//Custom event listener for a DB Collection after a 'get' request, return the documents collection
document.addEventListener('colFound', e => console.log(e.detail.msg));

//Custom event listener for a DB Change
document.addEventListener('docChanged', e => dbChg(e.detail));

//Pop tag
const popTag = (id, dbTag) => {
  const {
    Description,
    IOType,
    Name,
    Node,
    PinNo,
    PinTag,
    PinType,
    Schedule
  } = dbTag;

  //Pop tag element Box
  let tag = domOp({
    type: `div`,
    id: `${id}-tag`,
    cl: tag,
    par: tags
  });

  //Pop the tag name
  domOp({
    type: `textarea`,
    id: `${id}-tagName`,
    par: tag,
    cl: tagItem,
    val: Name
  });

  //Pop the tag description
  domOp({
    type: `textarea`,
    id: `${id}-tagDesc`,
    par: tag,
    cl: tagItem,
    val: Description
  });

  //Pop the tag description
  domOp({
    type: `textarea`,
    id: `${id}-tagDesc`,
    par: tag,
    cl: tagItem,
    val: Description
  });

  //Pop a edit icon with listener
  domOp({
    id: `${id}-edit`,
    type: 'i',
    cl: 'iconEdit fas fa-edit',
    par: eleTextBox,
    ev: 'click',
    evf: iconEditClicked
  });

  // Create update icon with listener
  domOp({
    id: `${id}-update`,
    type: 'i',
    cl: 'iconUpdate fas fa-sync-alt',
    par: eleTextBox,
    ev: 'click',
    evf: iconUpdateClicked
  });

  //Create add icon with listener
  domOp({
    id: `${id}-add`,
    type: 'i',
    cl: 'iconAdd fas fa-plus-circle',
    par: eleTextBox,
    ev: 'click',
    evf: iconAddClicked
  });

  //Create delete icon with listener
  domOp({
    id: `${id}-del`,
    type: 'i',
    cl: 'iconDelete fas fa-trash-alt',
    par: eleTextBox,
    ev: 'click',
    evf: iconDelClicked
  });
};

//**Pop the title, sub-title
const popTags = (title, currDir) => {
  // db = firebase.firestore();

  let body = document.getElementById('body');

  // doc Box
  const doc = domOp({
    type: `div`,
    id: `tags`,
    cl: `tags`,
    par: body
  });

  // Title
  let ele = domOp({
    type: `div`,
    id: `title`,
    cl: `title`,
    html: `${title}`,
    par: doc
  });

  //subTitle
  ele = domOp({
    type: `div`,
    id: `subTitle`,
    cl: `subTitle`,
    html: `${currDir}`,
    par: doc
  });
};

//************ Program *********************/

//Pop header

popTags('Title', 'sub-Title');

//Enable DB changes detection
// dbOp({ op: 'chg', col: 'Tags' });

//Get the documents for the current collection
// dbOp({ op: 'get', col: 'Tags' });

// console.log('dune');
