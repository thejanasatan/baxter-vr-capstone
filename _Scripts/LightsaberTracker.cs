using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LightsaberTracker : MonoBehaviour {

    private SteamVR_TrackedObject trackedObj;
    public GameObject lightsaber;
    private Lightsaber lightsaberScript;
    public GameObject lightsaberPrefab;
    [SerializeField] bool isPlayerController;

    [SerializeField]
    private UDPSend UDPScript;
    public GameObject network;

    private void Awake()
    {
        trackedObj = GetComponent<SteamVR_TrackedObject>();
        UDPScript = network.GetComponent<UDPSend>();
    }

    // Use this for initialization
    void Start () {
        lightsaber = Instantiate(lightsaberPrefab);
        lightsaber.transform.rotation = Quaternion.Euler(-90, 0, 0);
        lightsaber.transform.SetParent(gameObject.transform);
        lightsaber.GetComponentInChildren<Lightsaber>().isPlayerController = isPlayerController;

    }
	
	// Update is called once per frame
	void Update () {
        //lightsaber.transform.position = trackedObj.transform.position;// + new Vector3(0, 0.5f, 0);
        //lightsaber.transform.rotation = trackedObj.transform.rotation * Quaternion.Euler(270, 0, 0);
	}
}
