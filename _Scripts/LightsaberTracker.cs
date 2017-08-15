using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LightsaberTracker : MonoBehaviour {

    private SteamVR_TrackedObject trackedObj;
    private GameObject lightsaber;
    public GameObject lightsaberPrefab;

    [SerializeField]
    private UDPSend udpSendScript;
    public GameObject network;

    private void Awake()
    {
        trackedObj = GetComponent<SteamVR_TrackedObject>();
        udpSendScript = network.GetComponent<UDPSend>();
    }

    // Use this for initialization
    void Start () {
        lightsaber = Instantiate(lightsaberPrefab);
	}
	
	// Update is called once per frame
	void Update () {
        lightsaber.transform.position = trackedObj.transform.position;// + new Vector3(0, 0.5f, 0);
        lightsaber.transform.rotation = trackedObj.transform.rotation * Quaternion.Euler(270, 0, 0);
	}
}
