using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LightsaberController : MonoBehaviour {

    private SteamVR_TrackedObject trackedObj;
    private GameObject lightsaber;
    public GameObject lightsaberPrefab;

    private SteamVR_Controller.Device Controller
    {
        get { return SteamVR_Controller.Input((int)trackedObj.index); }
    }

    private void Awake()
    {
        trackedObj = GetComponent<SteamVR_TrackedObject>();
    }
    // Use this for initialization
    void Start () {
        lightsaber = Instantiate(lightsaberPrefab);
	}
	
	// Update is called once per frame
	void Update () {
        lightsaber.transform.position = trackedObj.transform.position;
        lightsaber.transform.rotation = trackedObj.transform.rotation * Quaternion.Euler(90, 0, 0);
	}
}
