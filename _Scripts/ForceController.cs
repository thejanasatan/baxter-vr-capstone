using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ForceController : MonoBehaviour {

	//public GameObject headMountedDisplay;

    private SteamVR_TrackedObject trackedObj;
    private Vector3 hitPoint;

    public GameObject targetObj;
    private Rigidbody targetRb;

	//public GameObject menuCanvas;

    [SerializeField] private float distOffset;
    public LayerMask forceMask;

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
		
	}
	
	// Update is called once per frame
	void Update () {
		if (Controller.GetHairTriggerDown() /*&& (SteamVR_Controller.GetDeviceIndex(SteamVR_Controller.DeviceRelation.Leftmost) == Controller.index)*/)
        {
            RaycastHit hit;
            Debug.Log("Trigger Down");

            if (Physics.Raycast(trackedObj.transform.position, transform.forward, out hit, 10,forceMask))
            {
                Debug.Log("Hit");
                targetObj = hit.transform.gameObject;
                distOffset = Vector3.Distance(hit.transform.position, transform.position);
                //distOffset = (hit.transform.position - transform.position);
                //targetObj.transform.position = transform.position;
            }
        }

        if (Controller.GetHairTriggerUp())
        {
            targetObj.GetComponent<Rigidbody>().velocity = Controller.velocity;
            targetObj.GetComponent<Rigidbody>().angularVelocity = Controller.angularVelocity;
            targetObj = null;
        }

        if (Controller.GetPress(SteamVR_Controller.ButtonMask.Touchpad) && targetObj != null)
        {
            Vector2 touchpad = (Controller.GetAxis(Valve.VR.EVRButtonId.k_EButton_Axis0));
            Debug.Log("Pressing Touchpad");

            if (touchpad.y > 0.7f)
            {
                Debug.Log("Farther");
                //distOffset += new Vector3(0, 0, 0.01f);
                if (distOffset < 5)
                {
                    distOffset += 0.025f / targetObj.GetComponent<Rigidbody>().mass;
                }
                
            }

            else if (touchpad.y < -0.7f)
            {
                Debug.Log("Closer");
                //distOffset += new Vector3(0, 0, -0.01f);
                
                if (distOffset > 1.2f/*targetObj.GetComponent<Renderer>().bounds.size*/)
                {
                    distOffset -= 0.025f / targetObj.GetComponent<Rigidbody>().mass;
                }
            }

            //if (touchpad.x > 0.7f)
            //{
            //    Debug.Log("Moving Right");

            //}

            //else if (touchpad.x < -0.7f)
            //{
            //    Debug.Log("Moving left");
            //}
        }

		if (Controller.GetHairTriggerDown())
		{
			//if (!menuCanvas.activeSelf)
			//{
			//	menuCanvas.SetActive (true);
			//	menuCanvas.transform.position = transform.position + new Vector3 (0, 0, 5);
			//	menuCanvas.transform.LookAt (headMountedDisplay.transform);
			//}
		}

        if (targetObj != null)
        {
            targetRb = targetObj.GetComponent<Rigidbody>();
            if (targetRb.velocity.x <= 0)
            {
                targetRb.velocity = new Vector3(0, targetRb.velocity.y, targetRb.velocity.z);
            }

            if  (targetRb.velocity.y <= 0)
            {
                targetRb.velocity = new Vector3(targetRb.velocity.x, 0, targetRb.velocity.z);
            }

            if (targetRb.velocity.z <= 0)
            {
                targetRb.velocity = new Vector3(targetRb.velocity.x, targetRb.velocity.z, 0);
            }

            if (targetRb.velocity.x > 0 || targetRb.velocity.y > 0 || targetRb.velocity.z > 0)
            {
                targetRb.velocity -= new Vector3(0.01f, 0.01f, 0.01f);
                targetRb.angularVelocity -= new Vector3(0.01f, 0.01f, 0.01f);
            }

            float speed = (10 / targetObj.GetComponent<Rigidbody>().mass) * Time.deltaTime;
            targetObj.transform.position = Vector3.MoveTowards(targetObj.transform.position, transform.position + transform.TransformDirection(new Vector3(0, 0, distOffset)), speed);
            //targetObj.transform.position = transform.position + transform.TransformDirection(new Vector3(0, 0, distOffset));
        }
    }
}
