// exportTags = () => {
const fetch = require('node-fetch');
//node-fetch does not look to work with local files so use URL of the file instead

const getTags = async () => {
  let res = await fetch(
    'http://dasdune/Projects/HomeAutomation/json/tags.json'
  );
  return await res.json();
  //   return data;
};

const getTags2 = async () => {
  await fetch(`https://api.github.com/users/${name}`).then(async (res) => {
    return await res.json();
  });
};

// getTags2();
getTags().then((data) => console.log(data));
// console.log(getTags2());
