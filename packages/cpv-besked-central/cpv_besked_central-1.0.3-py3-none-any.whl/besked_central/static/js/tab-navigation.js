const setCurrentActiveTab = (tabId) => {
  const tablinks = document.getElementsByClassName('tablinks');
  //re-set all to inactive
  for (const tab of tablinks) {
    tab.className = tab.className.replace(' active', '');
  }
  // activate current
  currentTab = document.getElementById(tabId);
  currentTab.className += ' active';
};

const openTab = (tab) => {
  if (!location.pathname.endsWith(tab)) {
    location.href = tab;
  }
};
