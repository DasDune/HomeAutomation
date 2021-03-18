const fetch = require('node-fetch');

// const data = { name: 'Tag6', description: 'This is Tag6' };

exportTag = tag => {
  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(tag)
    //body: tag
  };

  console.log(JSON.stringify(tag));

  fetch(
    'https://us-central1-homeautomation-654d6.cloudfunctions.net/setTag',
    options
  );
};

// exportTags = () => {
//node-fetch does not look to work with local files so use URL of the file instead
fetch('http://192.168.1.2/projects/HomeAutomation/json/tags.json')
  .then(function(res) {
    return res.json();
  })
  .then(data => {
    let output = '';
    data.map(tag => {
      console.log(tag);
      exportTag(tag);
    });
  })
  // .then(data => {
  //   console.log(data);
  // })
  .catch(err => {
    console.log(err);
  });
// };

exportNode = node => {
  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(node)
    //body: tag
  };

  console.log(JSON.stringify(node));

  fetch(
    'https://us-central1-homeautomation-654d6.cloudfunctions.net/setNode',
    options
  );
};

exportNodes = () => {
  //node-fetch does not look to work with local files so use URL of the file instead
  fetch('http://192.168.1.2/projects/HomeAutomation/json/nodes.json')
    .then(function(res) {
      return res.json();
    })
    .then(data => {
      let output = '';
      data.map(node => {
        console.log(node);
        exportNode(node);
      });
    })
    // .then(data => {
    //   console.log(data);
    // })
    .catch(err => {
      console.log(err);
    });
};

// exportTags();
