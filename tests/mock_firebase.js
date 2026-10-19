/* Nagebootste Firebase voor de tests (er wordt NIET met het echte project gepraat).
   Testgegevens komen uit window.__mockData: { "cafe/instellingen/toogscherm": true, ... }.
   Alles wat de pagina schrijft (set/update/remove/push/transaction) wordt bijgehouden in window.__mockSchrijf. */
(function () {
  window.__mockData = window.__mockData || {};
  window.__mockSchrijf = [];
  var teller = 0;

  // maakt een "snapshot" zoals Firebase die teruggeeft
  function snapshot(waarde, sleutel) {
    return {
      key: sleutel,
      val: function () { return waarde === undefined ? null : waarde; },
      forEach: function (cb) {
        if (waarde && typeof waarde === "object") {
          Object.keys(waarde).forEach(function (k) { cb(snapshot(waarde[k], k)); });
        }
      }
    };
  }

  function ref(pad) {
    var r = {
      key: pad.split("/").pop(),
      on: function (ev, cb) { setTimeout(function () { cb(snapshot(window.__mockData[pad], r.key)); }, 0); },
      off: function () {},
      set: function (v) { window.__mockSchrijf.push(["set", pad, v]); return Promise.resolve(); },
      update: function (v) { window.__mockSchrijf.push(["update", pad, v]); return Promise.resolve(); },
      remove: function () { window.__mockSchrijf.push(["remove", pad, null]); return Promise.resolve(); },
      push: function (v) {
        teller++;
        var kind = ref(pad + "/id" + teller); kind.key = "id" + teller;
        if (v !== undefined) window.__mockSchrijf.push(["push", pad, v]);
        return kind;
      },
      transaction: function (f) {
        var nieuw = f(window.__mockData[pad] === undefined ? null : window.__mockData[pad]);
        window.__mockSchrijf.push(["transaction", pad, nieuw]);
        return Promise.resolve({ committed: true, snapshot: snapshot(nieuw, r.key) });
      },
      orderByChild: function () { return r; },
      startAt: function () { return r; },
      equalTo: function () { return r; },
      limitToLast: function () { return r; }
    };
    return r;
  }

  var auth = {
    onAuthStateChanged: function (cb) { setTimeout(function () { cb({ uid: "testuid", isAnonymous: true }); }, 0); },
    signInAnonymously: function () { return Promise.resolve(); },
    signInWithEmailAndPassword: function () { return Promise.resolve(); },
    signOut: function () { return Promise.resolve(); }
  };
  window.firebase = {
    SDK_VERSION: "mock",
    initializeApp: function () {},
    auth: function () { return auth; },
    database: function () { return { ref: ref }; }
  };
  window.firebase.database.ServerValue = { TIMESTAMP: 1 };
})();
