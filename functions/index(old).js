const functions = require('firebase-functions');
const admin = require('firebase-admin');
// const gcs = require('@google-cloud/storage');
admin.initializeApp();

// // Create and Deploy Your First Cloud Functions
// // https://firebase.google.com/docs/functions/write-firebase-functions
//

// exports.generateThumbnail = functions.storage.object().onArchive(event => {
//   const object = event.data;
//   const filePath = object.name;
//   const fileName = filePath.split('/').pop();
//   const fileBucket = object.bucket;
//   const bucket = gcs.bucket(fileBucket);
//   const destPath = `/${fileName}`;

//   if (!object.contentType.startsWith('image/')) {
//     console.log('This is not an image.');
//     return;
//   }

//   if (object.resourceState === 'not_exists') {
//     console.log('This is a deletion event.');
//   }

//   return bucket.file(filePath).download({
//     destination: destPath
//   });
// });

// exports.api = functions.https.onRequest((req, res) => {
//   switch (req.url) {
//     case '/':
//       res.send('Welcome to Home Automation API!');
//       break;

//     case '/hehe':
//       res.send('hehe!');
//       break;

//     case '/nodes':
//       nodes = [];
//       admin
//         .firestore()
//         .collection('Nodes')
//         .get()
//         .then(snapshot => {
//           snapshot.docs.map(doc => {
//             nodes = [...nodes, doc.data()];
//           });
//           res.send(nodes);
//         })
//         .catch(error => {
//           console.log(error);
//           res.status(500).send(error);
//         });
//       break;

//     case '/tags':
//       tags = [];
//       admin
//         .firestore()
//         .collection('Tags')
//         .get()
//         .then(snapshot => {
//           snapshot.docs.map(doc => {
//             tags = [...tags, doc.data()];
//           });
//           res.send(tags);
//         })
//         .catch(error => {
//           console.log(error);
//           res.status(500).send(error);
//         });
//       break;

//     default:
//       res.send('Welcome to Home Automation API!');
//   }
// });

exports.hello = functions.https.onRequest((request, response) => {
  response.send('Hello from Firebase!');
});

exports.hello2 = functions.https.onRequest((request, response) => {
  const name = request.query.name;
  response.send('Hello ' + name + ' from Firebase!');
});

exports.hello3 = functions.https.onRequest((request, response) => {
  const name = request.body.name;
  response.send('Hello ' + name + ' from Firebase!');
});

exports.hello4 = functions.https.onRequest((request, response) => {
  const name = JSON.stringify(request.body);
  response.send('Hello ' + name + ' from Firebase!');
});

exports.sysInfo = functions.https.onRequest((req, res) => {
  admin
    .firestore()
    .collection('System')
    .get()
    .then(snapshot => {
      snapshot.docs.map(doc => {
        res.send(doc.data());
      });
    })
    .catch(error => {
      console.log(error);
      res.status(500).send(error);
    });
});

exports.getTag = functions.https.onRequest((request, response) => {
  const tag = request.query.tag;
  admin
    .firestore()
    .collection('Tags')
    .doc(tag)
    .get()
    .then(snapshot => {
      const data = snapshot.data();
      response.send(data);
    })
    .catch(erro => {
      console.log(error);
      response.status(500).send(error);
    });
});

exports.getTags = functions.https.onRequest((request, response) => {
  tags = [];
  admin
    .firestore()
    .collection('Tags')
    .get()
    .then(snapshot => {
      snapshot.docs.map(doc => {
        tags = [...tags, doc.data()];
      });
      response.send(tags);
    })
    .catch(error => {
      console.log(error);
      response.status(500).send(error);
    });
});

exports.getNodeTags = functions.https.onRequest((request, response) => {
  const node = request.query.node;
  tags = [];
  admin
    .firestore()
    .collection('Tags')
    .where('Node', '==', node)
    .get()
    .then(snapshot => {
      snapshot.docs.map(doc => {
        tags = [...tags, doc.data()];
      });
      response.send(tags);
    })
    .catch(error => {
      console.log(error);
      response.status(500).send(error);
    });
});

exports.setTag = functions.https.onRequest((request, response) => {
  const tag = request.body;
  // const tag = JSON.parse(request.body);
  // const tag = { name: 'Tag3', description: 'Description 3' };
  admin
    .firestore()
    .collection('Tags')
    .doc(tag.Name)
    .set(tag)
    .then(snapshot => {
      response.send('tag updated/created!');
    })
    .catch(error => {
      console.log(error);
      response.status(500).send(error);
    });
});

exports.getNode = functions.https.onRequest((request, response) => {
  const MAC = request.query.MAC;
  admin
    .firestore()
    .collection('Nodes')
    .doc(MAC)
    .get()
    .then(snapshot => {
      const data = snapshot.data();
      response.send(data);
    })
    .catch(erro => {
      console.log(error);
      response.status(500).send(error);
    });
});

exports.setNode = functions.https.onRequest((request, response) => {
  const node = request.body;
  // const tag = { name: 'Tag3', description: 'Description 3' };
  // response.send(node.MAC);
  admin
    .firestore()
    .collection('Nodes')
    .doc(node.MAC)
    .set(node)
    .then(snapshot => {
      response.send('node updated/created!');
    })
    .catch(error => {
      console.log(error);
      response.status(500).send(error);
    });
});
