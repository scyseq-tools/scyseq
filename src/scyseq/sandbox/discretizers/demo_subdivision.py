
import matplotlib.pyplot as plt

def henon_demo(nb_iter = 6, # Henon map
               init_cond = [0.63, 0.18],
               nb_pts=10000):

    henon = [init_cond]
    a, b = 1.4, 0.3
    for t in range(nb_pts):
        x, y = henon[t]
        henon.append([y + 1 - a * x**2., b*x])

    henon = np.array(henon)
#    xmin = np.min(henon[:, 0])
#    xmax = np.max(henon[:, 0])
#    ymin = np.min(henon[:, 1])
#    ymax = np.max(henon[:, 1])
    bb1, refs = subdivision(henon, nb_iter)

    # print refs
    cc = ['r.','c.','k.','b.','m.','g.','y.']

    for ii in np.arange(2**nb_iter):
        plt.plot(henon[bb1==ii, 0], henon[bb1==ii, 1], cc[ii%7])

#*!    # graphical min and max
#*!    xmin = -1.5
#*!    xmax = 1.5
#*!    ymin = -0.4
#*!    ymax = 0.4
#*!    # only for nb dim = 2 
#*!    boxes = [(0., 1., 0., 1.)] # xmin, xmax, ymin ymax
#*!    # yboxes = [(0., 1.)]
#*!    for n, rpoints in enumerate(refs):
#*!        # lref = refs[n]
#*!        # nb_ref = len(lref)
#*!        if n%2 == 0: # xsplit = axvline
#*!            print "xsplit"
#*!            next_boxes = []
#*!            for i, r in enumerate(rpoints):
#*!            # for nbox, xbox in enumerate(boxes):
#*!                frac = abs((r - ymin) / (ymax - ymin))
#*!                next_boxes.extend([(boxes[i/2][0], frac, boxes[i/2][2], boxes[i/2][3]), \
#*!                                    (frac, boxes[i/2][1], boxes[i/2][2], boxes[i/2][3])])
#*!                print r, boxes[i/2][2], boxes[i/2][3]
#*!                plt.axvline(x=r, ymin=boxes[i/2][2], ymax=boxes[i/2][3])
#*!            boxes = next_boxes
#*!                
#*!#            print yfrac
#*!#            lfrac = []
#*!#            for i, r in enumerate(rpoints):
#*!#                frac = abs((lref[i%nb_ref]-ymin) / (ymax - ymin))
#*!#                lfrac.append(frac)
#*!#                lymin = (i/2) * frac
#*!#                lymax = frac + (i/2) * (1- frac)
#*!#                print r, lymin, lymax
#*!#                plt.axvline(x=r, ymin=lymin, ymax=lymax)
#*!#            yfrac.extend(lfrac)
#*!#            print 'yfrac: ', yfrac
#*!
#*!        elif n%2 == 1: # ysplit = axhline
#*!            print 'ysplit'
#*!            next_boxes = []
#*!            # for nbox, ybox in enumerate(boxes):
#*!            for i, r in enumerate(rpoints):
#*!                # frac = abs((lref[nbox%nb_ref]-xmin) / (xmax - xmin))
#*!                frac = abs((r - xmin) / (xmax - xmin))
#*!                nbbox = len(boxes)
#*!                next_boxes.extend([(boxes[i%nbbox][0], boxes[i%nbbox][1],
#*!                    boxes[i%nbbox][2], frac), 
#*!                                    (boxes[i%nbbox][0], boxes[i%nbbox][1], frac,
#*!                                        boxes[i%nbbox][3])])
#*!                print r, boxes[i%nbbox][0], boxes[i%nbbox][1]
#*!                # plt.axhline(y=lref[nbox], xmin=boxes[nbox][0], xmax=boxes[nbox][1])
#*!                plt.axhline(y=r, xmin=boxes[i%nbbox][0], xmax=boxes[i%nbbox][1])
#*!            boxes = next_boxes
#*!#            lfrac = []
#*!#            print xfrac
#*!#            for i, r in enumerate(rpoints):
#*!#                frac = abs((lref[i%nb_ref]-xmin) / (xmax - xmin))
#*!#                lfrac.append(frac)
#*!#                print i/2, frac
#*!#                lxmin = (i%2) * frac
#*!#                lxmax = frac + (i%2) * (1- frac)
#*!#                print r, lxmin, lxmax
#*!#                plt.axhline(y=r, xmin=lxmin, xmax=lxmax)
#*!#            xfrac.extend(lfrac)
#*!#            print 'xfrac: ', xfrac
#*!
#*!#            # ind = n/2; print ind
#*!#            try:
#*!#                lymin = abs((yref[n%2]-ymin)/(ymax-ymin))
#*!#            except:
#*!#                lymin = abs((yref[0]-ymin)/(ymax-ymin))
#*!#            lymax = 1.
#*!#        print "xref: ", r, " ymin: ", lymin, " ymax: ", lymax
#*!#        plt.axvline(x=r, ymin=lymin, ymax=lymax)
#*!#    xref = refs[jj]
#*!#    yref = refs[jj]
    plt.show()
